<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

final class Version20260603000001 extends AbstractMigration
{
    public function getDescription(): string
    {
        return 'Create document table';
    }

    public function up(Schema $schema): void
    {
        $this->addSql(<<<'SQL'
            CREATE TABLE document (
                id UUID NOT NULL,
                original_filename VARCHAR(255) NOT NULL,
                s3_key VARCHAR(500) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pending',
                provider VARCHAR(20) NOT NULL DEFAULT 'claude',
                created_at TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
                processed_at TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT NULL,
                PRIMARY KEY(id)
            )
        SQL);

        $this->addSql("COMMENT ON COLUMN document.id IS '(DC2Type:uuid)'");
        $this->addSql("COMMENT ON COLUMN document.created_at IS '(DC2Type:datetime_immutable)'");
        $this->addSql("COMMENT ON COLUMN document.processed_at IS '(DC2Type:datetime_immutable)'");
    }

    public function down(Schema $schema): void
    {
        $this->addSql('DROP TABLE document');
    }
}
