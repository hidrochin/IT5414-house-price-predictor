# 🏠 IT5414 - House Price Predictor

Dự án Machine Learning end-to-end dự đoán giá nhà, áp dụng các nguyên tắc MLOps.

---

## 📦 Cấu trúc dự án

```
IT5414-house-price-predictor/
├── .github/
│   └── workflows/
│       └── ci.yaml             # GitHub Actions CI workflow
├── configs/                    # Cấu hình model
│   └── model_config.yaml
├── data/
│   ├── raw/                    # Dữ liệu gốc
│   └── processed/              # Dữ liệu đã xử lý
├── deployment/
│   ├── argocd/                 # ArgoCD Application config
│   ├── kubernetes/             # K8s manifests (api, ui, namespace)
│   ├── mlflow/                 # Docker Compose cho MLflow
│   └── monitoring/             # Prometheus & Grafana configs
├── models/
│   └── trained/                # Model và preprocessor đã train
├── notebooks/                  # Jupyter notebooks thử nghiệm
├── src/
│   ├── api/                    # FastAPI backend (with Prometheus metrics)
│   ├── data/                   # Script xử lý dữ liệu
│   ├── features/               # Feature engineering
│   └── models/                 # Training scripts
├── streamlit_app/              # Giao diện Streamlit
├── tests/                      # Unit tests
├── Dockerfile                  # Docker cho FastAPI
├── docker-compose.yaml         # Orchestration (API, UI, Prometheus, Grafana)
└── requirements.txt
```


---

## 🛠️ Yêu cầu hệ thống

- **Python**: 3.10 hoặc 3.11
- **Docker Desktop**: [Download](https://www.docker.com/products/docker-desktop/)
- **Git**: [Download](https://git-scm.com/)
- **Anaconda/Miniconda** (khuyến nghị): [Download](https://docs.conda.io/en/latest/miniconda.html)

---

## 🚀 Hướng dẫn cài đặt và chạy

### Bước 1: Clone repository

```bash
git clone https://github.com/hidrochin/IT5414-house-price-predictor
cd IT5414-house-price-predictor
```

### Bước 2: Tạo môi trường Python

```bash
# Sử dụng Conda (khuyến nghị)
conda create -n it5414 python=3.10
conda activate it5414

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 3: Cài đặt Docker Desktop

1. Tải Docker Desktop tại https://www.docker.com/products/docker-desktop/
2. Chọn **Download for Windows – AMD64**
3. Cài đặt với tùy chọn **Use WSL 2**
4. Khởi động Docker Desktop
5. Kiểm tra: `docker --version`

### Bước 4: Khởi động MLflow

```bash
cd deployment/mlflow
docker compose up -d
```

Truy cập MLflow UI: http://localhost:5555

### Bước 5: Training Model

```bash
# Quay lại thư mục gốc
cd ../..

# 1. Xử lý dữ liệu
python src/data/run_processing.py \
  --input data/raw/house_data.csv \
  --output data/processed/cleaned_house_data.csv

# 2. Feature engineering
python src/features/engineer.py \
  --input data/processed/cleaned_house_data.csv \
  --output data/processed/featured_house_data.csv \
  --preprocessor models/trained/preprocessor.pkl

# 3. Train model
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models \
  --mlflow-tracking-uri http://localhost:5555
```

### Bước 6: Chạy ứng dụng với Docker

```bash
# Build và khởi động
docker compose up -d

# Kiểm tra trạng thái
docker ps
```

---

## 🌐 Truy cập ứng dụng

| Dịch vụ | URL | Mô tả |
|---------|-----|-------|
| **Streamlit UI** | http://localhost:8501 | Giao diện người dùng |
| **FastAPI** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger documentation |
| **MLflow** | http://localhost:5555 | Experiment tracking |

---

## 📡 Sử dụng API

### Health Check

```bash
curl http://localhost:8000/health
```

### Dự đoán giá nhà

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sqft": 1500,
    "bedrooms": 3,
    "bathrooms": 2,
    "location": "suburban",
    "year_built": 2000,
    "condition": "Good"
  }'
```

**Response:**
```json
{
  "predicted_price": 382536.69,
  "confidence_interval": [344283.02, 420790.36],
  "features_importance": {},
  "prediction_time": "2025-12-14T03:45:41"
}
```

---

## 🔄 Quản lý Docker

```bash
# Xem logs
docker compose logs -f

# Dừng tất cả containers
docker compose down

# Rebuild sau khi sửa code
docker compose build
docker compose up -d
```

---

## 📁 Các file quan trọng

| File | Mô tả |
|------|-------|
| `Dockerfile` | Build FastAPI backend |
| `streamlit_app/Dockerfile` | Build Streamlit frontend |
| `docker-compose.yaml` | Orchestrate cả 2 services |
| `configs/model_config.yaml` | Cấu hình model (algorithm, hyperparameters) |
| `models/trained/house_price_model.pkl` | Model đã train |
| `models/trained/preprocessor.pkl` | Preprocessor cho features |

---

## 🧪 Model Performance

- **Algorithm**: GradientBoosting
- **MAE**: 6,879.37
- **R² Score**: 0.9985

---

## 🔄 CI/CD Pipeline

### GitHub Actions (CI)

Workflow tự động chạy khi push/PR vào `main`:

```yaml
# .github/workflows/ci.yaml
Jobs:
  1. Lint & Format Check (flake8, black)
  2. Run Tests (pytest)
  3. Build Docker Images
  4. Push to GitHub Container Registry
```

**Xem CI runs:** https://github.com/hidrochin/IT5414-house-price-predictor/actions

### ArgoCD (CD)

GitOps-based deployment với Kubernetes:

```bash
# Cài đặt ArgoCD (nếu có K8s cluster)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy ứng dụng
kubectl apply -f deployment/argocd/application.yaml
```

**Kubernetes manifests:**
- `deployment/kubernetes/namespace.yaml` - Namespace
- `deployment/kubernetes/api/` - FastAPI Deployment & Service
- `deployment/kubernetes/ui/` - Streamlit Deployment & Service

---

## 📊 Monitoring với Prometheus & Grafana

### Khởi động Monitoring Stack

```bash
docker compose up -d
```

### Truy cập Monitoring

| Dịch vụ | URL | Credentials |
|---------|-----|-------------|
| **Prometheus** | http://localhost:9090 | N/A |
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **API Metrics** | http://localhost:8000/metrics | N/A |

### Metrics được thu thập

- `http_requests_total` - Tổng số requests
- `http_request_duration_seconds` - Latency (p50, p95, p99)
- `prediction_requests_total` - Số lượng predictions
- `prediction_latency_seconds` - Thời gian xử lý prediction

### Cấu trúc Monitoring

```
deployment/monitoring/
├── prometheus/
│   └── prometheus.yaml          # Scrape config
└── grafana/
    └── provisioning/
        ├── dashboards/
        │   └── house-price-api.json  # Dashboard
        └── datasources/
            └── datasources.yaml      # Prometheus datasource
```

---

## 🧪 Testing

```bash
# Cài đặt test dependencies
pip install pytest httpx

# Chạy tests
pytest tests/ -v

# Chạy tests với coverage
pytest tests/ -v --cov=src/api
```

---

## 👨‍💻 Thành viên nhóm



## 📝 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

**IT5414 - Machine Learning Course Project**
