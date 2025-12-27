"""
Script to download model from MLflow Model Registry.
Used during Docker build or at container startup.
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_from_mlflow():
    """Download model and preprocessor from MLflow Registry."""
    try:
        import mlflow
        from mlflow.tracking import MlflowClient

        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5555")
        model_name = os.getenv("MODEL_NAME", "house_price_model")
        model_stage = os.getenv("MODEL_STAGE", "Staging")
        output_dir = os.getenv("MODEL_OUTPUT_DIR", "./models/trained")

        logger.info(f"Connecting to MLflow at: {tracking_uri}")
        mlflow.set_tracking_uri(tracking_uri)
        client = MlflowClient()

        # Get latest version in the specified stage
        logger.info(f"Looking for model '{model_name}' in stage '{model_stage}'")
        versions = client.get_latest_versions(model_name, stages=[model_stage])

        if not versions:
            logger.warning(f"No model found in stage '{model_stage}'. Trying 'Production'...")
            versions = client.get_latest_versions(model_name, stages=["Production"])

        if not versions:
            logger.error(f"No model versions found for '{model_name}'")
            return False

        model_version = versions[0]
        logger.info(f"Found model version {model_version.version} in stage {model_version.current_stage}")

        # Download model
        model_uri = f"models:/{model_name}/{model_stage}"
        logger.info(f"Downloading model from: {model_uri}")

        os.makedirs(output_dir, exist_ok=True)

        # Download the sklearn model
        model = mlflow.sklearn.load_model(model_uri)

        import joblib

        model_path = os.path.join(output_dir, f"{model_name}.pkl")
        joblib.dump(model, model_path)
        logger.info(f"Saved model to: {model_path}")

        return True

    except Exception as e:
        logger.error(f"Failed to download model from MLflow: {e}")
        logger.info("Checking for local model files...")

        # Check if local files exist
        model_path = os.path.join(output_dir, f"{model_name}.pkl")
        if os.path.exists(model_path):
            logger.info(f"Local model found at: {model_path}")
            return True

        return False


if __name__ == "__main__":
    success = download_from_mlflow()
    sys.exit(0 if success else 1)
