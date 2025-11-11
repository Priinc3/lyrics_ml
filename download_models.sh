#!/bin/bash
# Download pre-trained model artifacts on first run

ARTIFACTS_DIR="artifacts"
mkdir -p "$ARTIFACTS_DIR"

# List of artifacts to download (GitHub releases)
REPO="Priinc3/lyrics_ml"
RELEASE_TAG="v1.0-models"

echo "📥 Downloading pre-trained models..."

# URLs (will be set after first release)
artifacts=(
    "pipeline_lr.joblib"
    "svd_200.joblib"
)

for artifact in "${artifacts[@]}"; do
    if [ ! -f "$ARTIFACTS_DIR/$artifact" ]; then
        echo "   Downloading $artifact..."
        # Placeholder: replace with actual download link after GitHub release
        # curl -L -o "$ARTIFACTS_DIR/$artifact" "https://github.com/$REPO/releases/download/$RELEASE_TAG/$artifact"
        echo "   ⚠️  $artifact not found. Please download from: https://github.com/$REPO"
    fi
done

echo "✅ Artifacts check complete"
