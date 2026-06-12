import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api.utils.classifier import classify_issue, get_priority_level, suggest_department
from api.utils.duplicate_detector import preprocess_text, jaccard_similarity, cosine_similarity
from api.utils.priority_scorer import calculate_priority_score, get_priority_color, get_priority_label


class TestClassifier:
    def test_classify_road_issue(self):
        category, confidence, department = classify_issue(
            "Pothole on Main Street",
            "There is a large pothole in the middle of the road causing traffic"
        )
        assert category == "Road Maintenance"
        assert confidence > 0.2
        assert department == "Road Maintenance"

    def test_classify_electricity_issue(self):
        category, confidence, department = classify_issue(
            "Power outage in neighborhood",
            "The street lights are not working and we have no electricity"
        )
        assert category == "Electricity"
        assert confidence > 0.3

    def test_classify_water_issue(self):
        category, confidence, department = classify_issue(
            "Water pipe leak",
            "There is water leaking from the pipe on the sidewalk"
        )
        assert category == "Water Supply"
        assert confidence > 0.2

    def test_classify_waste_issue(self):
        category, confidence, department = classify_issue(
            "Garbage not collected",
            "The trash bins have been overflowing for days"
        )
        assert category == "Waste Management"
        assert confidence > 0.3

    def test_classify_unspecified(self):
        category, confidence, department = classify_issue(
            "Hello",
            "How are you"
        )
        assert category == "Unspecified"
        assert confidence == 0.0

    def test_priority_critical(self):
        level, score = get_priority_level(
            "Danger gas leak on 5th Avenue",
            "There is a dangerous gas leak that could cause an explosion",
            upvote_count=0
        )
        assert level in ["critical", "high"]
        assert score >= 40

    def test_priority_high(self):
        level, score = get_priority_level(
            "Broken street light",
            "The street light is not working and it's dark at night",
            upvote_count=5
        )
        assert level in ["high", "critical"]

    def test_priority_with_upvotes(self):
        level1, score1 = get_priority_level("Issue", "Some problem", upvote_count=0)
        level2, score2 = get_priority_level("Issue", "Some problem", upvote_count=10)
        assert score2 > score1

    def test_suggest_department(self):
        dept = suggest_department("Road Maintenance", 0.5)
        assert dept == "Road Maintenance"

    def test_suggest_department_low_confidence(self):
        dept = suggest_department("Unspecified", 0.1)
        assert dept is None


class TestDuplicateDetector:
    def test_preprocess_text(self):
        words = preprocess_text("This is a test message about roads")
        assert "test" in words
        assert "roads" in words
        assert "is" not in words
        assert "the" not in words

    def test_jaccard_similarity_identical(self):
        s = {"pothole", "road", "damage"}
        assert jaccard_similarity(s, s) == 1.0

    def test_jaccard_similarity_disjoint(self):
        s1 = {"pothole", "road"}
        s2 = {"water", "pipe"}
        assert jaccard_similarity(s1, s2) == 0.0

    def test_jaccard_similarity_partial(self):
        s1 = {"pothole", "road", "damage"}
        s2 = {"road", "damage", "repair"}
        sim = jaccard_similarity(s1, s2)
        assert 0.0 < sim < 1.0

    def test_cosine_similarity_identical(self):
        s = {"pothole", "road", "damage"}
        assert cosine_similarity(s, s) > 0.9

    def test_cosine_similarity_empty(self):
        assert cosine_similarity(set(), {"a", "b"}) == 0.0


class TestPriorityScorer:
    def test_critical_priority(self):
        level, score, breakdown = calculate_priority_score(
            issue_type="Electricity",
            title="Danger: gas leak",
            description="There is a dangerous gas leak that could cause an explosion",
            upvote_count=0,
            comment_count=0,
            has_images=True
        )
        assert level in ["critical", "high"]
        assert score > 30

    def test_low_priority(self):
        level, score, breakdown = calculate_priority_score(
            issue_type="Waste Management",
            title="Minor request",
            description="Would like a new trash bin please",
            upvote_count=0,
            comment_count=0,
            has_images=False
        )
        assert level in ["low", "medium"]
        assert score < 50

    def test_upvotes_increase_priority(self):
        _, score1, _ = calculate_priority_score(
            issue_type="Road Maintenance",
            title="Road issue",
            description="Some road problem",
            upvote_count=0
        )
        _, score2, _ = calculate_priority_score(
            issue_type="Road Maintenance",
            title="Road issue",
            description="Some road problem",
            upvote_count=20
        )
        assert score2 > score1

    def test_images_increase_priority(self):
        _, score1, _ = calculate_priority_score(
            issue_type="Road Maintenance",
            title="Road issue",
            description="Some road problem",
            has_images=False
        )
        _, score2, _ = calculate_priority_score(
            issue_type="Road Maintenance",
            title="Road issue",
            description="Some road problem",
            has_images=True
        )
        assert score2 > score1

    def test_priority_color(self):
        assert get_priority_color("critical") == "#dc2626"
        assert get_priority_color("high") == "#ea580c"
        assert get_priority_color("medium") == "#ca8a04"
        assert get_priority_color("low") == "#16a34a"

    def test_priority_label(self):
        assert get_priority_label("critical") == "Critical"
        assert get_priority_label("high") == "High"
        assert get_priority_label("medium") == "Medium"
        assert get_priority_label("low") == "Low"
