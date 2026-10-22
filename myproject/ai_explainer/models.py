from django.db import models


class TermCache(models.Model):
    class Source(models.TextChoices):
        SEED = "seed", "Seed"
        GEMINI = "gemini", "Gemini"

    term_normalized = models.CharField(max_length=60, unique=True)
    explanation = models.TextField()
    source = models.CharField(max_length=8, choices=Source.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "AI term cache"
        verbose_name_plural = "AI term cache"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(source__in=["seed", "gemini"]),
                name="aiterm_source_seed_or_gemini",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.term_normalized} ({self.source})"
