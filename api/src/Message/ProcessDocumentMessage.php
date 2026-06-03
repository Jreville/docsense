<?php

namespace App\Message;

/**
 * Message publié dans SQS après chaque upload.
 * Le worker Python le consomme pour lancer l'extraction IA.
 */
final class ProcessDocumentMessage
{
    public function __construct(
        public readonly string $documentId,
        public readonly string $s3Key,
        public readonly string $provider,
    ) {}
}
