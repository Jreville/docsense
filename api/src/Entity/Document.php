<?php

namespace App\Entity;

use ApiPlatform\Metadata\ApiResource;
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\GetCollection;
use ApiPlatform\Metadata\Post;
use App\Enum\DocumentStatus;
use App\Enum\LlmProvider;
use App\Repository\DocumentRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Uid\Uuid;

#[ORM\Entity(repositoryClass: DocumentRepository::class)]
#[ORM\HasLifecycleCallbacks]
#[ApiResource(
    operations: [
        new Get(),
        new GetCollection(),
    ]
)]
class Document
{
    #[ORM\Id]
    #[ORM\Column(type: 'uuid', unique: true)]
    #[ORM\GeneratedValue(strategy: 'CUSTOM')]
    #[ORM\CustomIdGenerator(class: 'doctrine.uuid_generator')]
    private Uuid $id;

    #[ORM\Column(length: 255)]
    private string $originalFilename;

    #[ORM\Column(length: 500)]
    private string $s3Key;

    #[ORM\Column(length: 20, enumType: DocumentStatus::class)]
    private DocumentStatus $status = DocumentStatus::Pending;

    #[ORM\Column(length: 20, enumType: LlmProvider::class)]
    private LlmProvider $provider = LlmProvider::Claude;

    #[ORM\Column]
    private \DateTimeImmutable $createdAt;

    #[ORM\Column(nullable: true)]
    private ?\DateTimeImmutable $processedAt = null;

    #[ORM\PrePersist]
    public function initCreatedAt(): void
    {
        $this->createdAt = new \DateTimeImmutable();
    }

    // Getters & setters

    public function getId(): Uuid
    {
        return $this->id;
    }

    public function getOriginalFilename(): string
    {
        return $this->originalFilename;
    }

    public function setOriginalFilename(string $originalFilename): static
    {
        $this->originalFilename = $originalFilename;
        return $this;
    }

    public function getS3Key(): string
    {
        return $this->s3Key;
    }

    public function setS3Key(string $s3Key): static
    {
        $this->s3Key = $s3Key;
        return $this;
    }

    public function getStatus(): DocumentStatus
    {
        return $this->status;
    }

    public function setStatus(DocumentStatus $status): static
    {
        $this->status = $status;
        return $this;
    }

    public function getProvider(): LlmProvider
    {
        return $this->provider;
    }

    public function setProvider(LlmProvider $provider): static
    {
        $this->provider = $provider;
        return $this;
    }

    public function getCreatedAt(): \DateTimeImmutable
    {
        return $this->createdAt;
    }

    public function getProcessedAt(): ?\DateTimeImmutable
    {
        return $this->processedAt;
    }

    public function setProcessedAt(?\DateTimeImmutable $processedAt): static
    {
        $this->processedAt = $processedAt;
        return $this;
    }
}
