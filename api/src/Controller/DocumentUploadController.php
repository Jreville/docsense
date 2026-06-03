<?php

namespace App\Controller;

use App\Entity\Document;
use App\Enum\LlmProvider;
use App\Message\ProcessDocumentMessage;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Messenger\MessageBusInterface;
use Symfony\Component\Routing\Attribute\Route;

class DocumentUploadController extends AbstractController
{
    public function __construct(
        private readonly EntityManagerInterface $em,
        private readonly MessageBusInterface $bus,
    ) {}

    #[Route('/documents', name: 'document_upload', methods: ['POST'])]
    public function upload(Request $request): JsonResponse
    {
        $file = $request->files->get('file');

        if (!$file) {
            return $this->json(['error' => 'Aucun fichier reçu.'], Response::HTTP_BAD_REQUEST);
        }

        $allowedMimeTypes = ['application/pdf', 'text/csv', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!in_array($file->getMimeType(), $allowedMimeTypes, true)) {
            return $this->json(['error' => 'Type de fichier non supporté. Formats acceptés : PDF, CSV, DOCX.'], Response::HTTP_UNPROCESSABLE_ENTITY);
        }

        // Résolution du provider (défaut : claude)
        $providerValue = $request->request->get('provider', 'claude');
        $provider = LlmProvider::tryFrom($providerValue) ?? LlmProvider::Claude;

        // Stockage local (var/uploads/) — sera remplacé par S3 à l'étape docker-compose
        $uploadDir = $this->getParameter('kernel.project_dir') . '/var/uploads';
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0755, true);
        }

        $safeFilename = uniqid('doc_', true) . '.' . $file->guessExtension();
        $file->move($uploadDir, $safeFilename);
        $s3Key = 'uploads/' . $safeFilename;

        // Persistance en base
        $document = (new Document())
            ->setOriginalFilename($file->getClientOriginalName())
            ->setS3Key($s3Key)
            ->setProvider($provider);

        $this->em->persist($document);
        $this->em->flush();

        // Publication du message dans SQS via Messenger
        $this->bus->dispatch(new ProcessDocumentMessage(
            documentId: (string) $document->getId(),
            s3Key:      $s3Key,
            provider:   $provider->value,
        ));

        return $this->json([
            'id'       => (string) $document->getId(),
            'filename' => $document->getOriginalFilename(),
            'status'   => $document->getStatus()->value,
            'provider' => $document->getProvider()->value,
        ], Response::HTTP_CREATED);
    }
}
