"""
Quality assessment domain models for olive oil quality control.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from .spectrum import Spectrum


class QualityGrade(Enum):
    """Quality grades for olive oil."""
    EXTRA_VIRGIN = "extra_virgin"
    VIRGIN = "virgin"
    LAMPANTE = "lampante"
    REFINED = "refined"
    UNKNOWN = "unknown"


class QualityIndicator(Enum):
    """Quality indicators for olive oil."""
    ACIDITY = "acidity"
    PEROXIDE_VALUE = "peroxide_value"
    K232 = "k232"
    K270 = "k270"
    DELTA_K = "delta_k"
    FLAVOR = "flavor"
    AROMA = "aroma"


@dataclass
class QualityMetrics:
    """Quality metrics for olive oil assessment."""
    acidity: Optional[float] = None  # Free fatty acid content (%)
    peroxide_value: Optional[float] = None  # Peroxide value (meq O2/kg)
    k232: Optional[float] = None  # UV absorption at 232 nm
    k270: Optional[float] = None  # UV absorption at 270 nm
    delta_k: Optional[float] = None  # Delta K value
    flavor_score: Optional[float] = None  # Sensory evaluation score
    aroma_score: Optional[float] = None  # Aroma evaluation score
    timestamp: Optional[datetime] = None
    
    def calculate_overall_score(self) -> float:
        """Calculate an overall quality score based on all metrics."""
        scores = []
        
        # Acidity score (lower is better, max 0.8% for extra virgin)
        if self.acidity is not None:
            if self.acidity <= 0.8:
                scores.append(100 - (self.acidity / 0.8) * 20)  # 80-100 points
            else:
                scores.append(max(0, 80 - (self.acidity - 0.8) * 50))  # Decreasing score
        
        # Peroxide value score (lower is better, max 20 meq/kg for extra virgin)
        if self.peroxide_value is not None:
            if self.peroxide_value <= 20:
                scores.append(100 - (self.peroxide_value / 20) * 20)  # 80-100 points
            else:
                scores.append(max(0, 80 - (self.peroxide_value - 20) * 2))
        
        # K232 score (lower is better, max 2.5 for extra virgin)
        if self.k232 is not None:
            if self.k232 <= 2.5:
                scores.append(100 - (self.k232 / 2.5) * 20)  # 80-100 points
            else:
                scores.append(max(0, 80 - (self.k232 - 2.5) * 20))
        
        # K270 score (lower is better, max 0.22 for extra virgin)
        if self.k270 is not None:
            if self.k270 <= 0.22:
                scores.append(100 - (self.k270 / 0.22) * 20)  # 80-100 points
            else:
                scores.append(max(0, 80 - (self.k270 - 0.22) * 200))
        
        # Sensory scores
        if self.flavor_score is not None:
            scores.append(self.flavor_score)
        
        if self.aroma_score is not None:
            scores.append(self.aroma_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def determine_quality_grade(self) -> QualityGrade:
        """Determine quality grade based on metrics."""
        overall_score = self.calculate_overall_score()
        
        if overall_score >= 90:
            return QualityGrade.EXTRA_VIRGIN
        elif overall_score >= 80:
            return QualityGrade.VIRGIN
        elif overall_score >= 60:
            return QualityGrade.LAMPANTE
        else:
            return QualityGrade.REFINED


@dataclass
class QualityThreshold:
    """Quality thresholds for different grades."""
    grade: QualityGrade
    max_acidity: float
    max_peroxide_value: float
    max_k232: float
    max_k270: float
    min_flavor_score: float
    min_aroma_score: float
    
    def check_compliance(self, metrics: QualityMetrics) -> Dict[str, bool]:
        """Check if metrics comply with this threshold."""
        compliance = {}
        
        if metrics.acidity is not None:
            compliance['acidity'] = metrics.acidity <= self.max_acidity
        
        if metrics.peroxide_value is not None:
            compliance['peroxide_value'] = metrics.peroxide_value <= self.max_peroxide_value
        
        if metrics.k232 is not None:
            compliance['k232'] = metrics.k232 <= self.max_k232
        
        if metrics.k270 is not None:
            compliance['k270'] = metrics.k270 <= self.max_k270
        
        if metrics.flavor_score is not None:
            compliance['flavor'] = metrics.flavor_score >= self.min_flavor_score
        
        if metrics.aroma_score is not None:
            compliance['aroma'] = metrics.aroma_score >= self.min_aroma_score
        
        return compliance


@dataclass
class SpectralQualityAssessment:
    """Quality assessment based on spectral data."""
    spectrum: Spectrum
    quality_metrics: QualityMetrics
    quality_grade: QualityGrade
    spectral_features: Optional[Dict[str, float]] = None
    assessment_confidence: Optional[float] = None
    assessment_method: Optional[str] = None
    timestamp: Optional[datetime] = None
    
    def is_acceptable_quality(self, min_grade: QualityGrade = QualityGrade.VIRGIN) -> bool:
        """Check if the quality meets minimum requirements."""
        grade_hierarchy = {
            QualityGrade.EXTRA_VIRGIN: 4,
            QualityGrade.VIRGIN: 3,
            QualityGrade.LAMPANTE: 2,
            QualityGrade.REFINED: 1,
            QualityGrade.UNKNOWN: 0
        }
        
        return grade_hierarchy[self.quality_grade] >= grade_hierarchy[min_grade] 