<?php

namespace App\Enum;

enum LlmProvider: string
{
    case Claude  = 'claude';
    case Mistral = 'mistral';
}
