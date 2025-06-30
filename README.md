# HydrauLink

**HydrauLink** - Hydraulic Press Your Link

HydrauLink 是一款簡潔實用的 **短網址生成平台**，靈感來自液壓機 hydraulic press 與 link 結合的概念，讓冗長連結瞬間壓縮成可控短碼。支援自訂短碼、密碼保護、短網址管理與安全驗證，並結合美觀的 UI 設計與 Redis 速率限制防止濫用。

---

## 專案特色

**Docker 容器化**：完整支援 Docker 開發與部署，包含 PostgreSQL + Redis + Django。
**Test-Driven Development**：採用 Pytest + Django plugin 撰寫測試，確保品質。
**支援密碼保護**：使用者可為短網址加上密碼，保障安全性。
**自訂短碼**：可自選自訂 slug，長度限制 6–8 字。
**自動抓取網站簡介**：使用 `og:description` / `meta[name=description]` / `<title>` 自動補上連結簡介。
**連結安全檢查**：整合 Google Safe Browsing API 驗證原始網址。
**防止濫用**：以 Redis 快取實作 IP 每分鐘限流（最多 5 次）。
**點擊次數追蹤**：每次轉址都會記錄 click count。
**前端整合**：使用 Tailwind CSS + DaisyUI 打造美觀介面，支援 Alpine.js 動態互動。

---

## 專案架構

```
HydrauLink/
├── config/                 # Django 設定模組
├── press/                  # 主功能 app：短網址生成、轉址、表單處理、工具模組
│   ├── views.py
│   ├── urls.py
│   ├── utils/              # 各種輔助功能（slug 產生、描述爬蟲、安全驗證、速率限制）
│   ├── tests/              # 各種測試功能
│   └── templates/press/    # 首頁模板
├── users/                  # 使用者登入、管理功能
├── static/                 # 靜態資源（背景圖等）
├── templates/shared/       # 共用模板（base.html 等）
├── Dockerfile.dev          # 開發用 Dockerfile
├── docker-compose.yml      # 開發用 Docker Compose 設定
├── Dockerfile              # 部屬用 Dockerfile
├── docker-compose.prod.yml # 部屬用 Docker Compose 設定
├── main.py                 # 入口點（uv run）
├── pyproject.toml          # 使用 uv 套件管理的配置檔
├── uv.lock
├── .env.example            # 環境變數範例
└── README.md               # 專案說明
```

---

## 開發環境設定

### 安裝依賴（使用 [`uv`](https://github.com/astral-sh/uv)）

```bash
uv init
uv venv
```
```
docker compose exec web uv add 套件名稱
uv sync
```

### 啟動開發容器

```bash
docker compose up --build
docker compose exec web uv run python manage.py migrate
```

### 建立管理者帳號

```bash
docker compose exec web uv run python manage.py createsuperuser
```

---

## 核心功能設計

### 1. 建立短網址

* 表單：首頁 `/`
* 欄位：原始網址、短碼（可選，未填自動生成）、密碼（可選，未填不加密）
* 驗證：

  * URL 格式與安全性
  * Slug 僅允許 6–8 字元英數字
  * 密碼格式同上

### 2. 頁面資訊抓取（`/note/`）

* 由 `fetch_description()` 進行網頁爬蟲，抓取 meta 描述或標題
* 若無則顯示「無簡介」

### 3. 轉址與密碼驗證（`/<slug>/`）

* 若有設定密碼則先跳轉至 `/press/password.html`
* 若正確或未設定密碼則執行：

  * click_count += 1
  * redirect 到原始連結

### 4. Redis 限速邏輯

* 每個 IP 每分鐘最多提交 5 次
* 超過則直接回傳錯誤

---

## 測試方式

本專案採用 **Pytest** + `pytest-django` 撰寫測試，覆蓋關鍵流程。

```bash
docker compose exec web uv run pytest
```

測試位於 `press/tests/` 內，涵蓋：

* 建立短網址流程
* 密碼保護與驗證
* 描述擷取 fallback 邏輯
* 轉址成功與錯誤處理
* Slug 衝突與格式錯誤處理

---

## 部署建議（Production）

請使用 `docker-compose.prod.yml` 並搭配：

* gunicorn
* 設定 HTTPS 與網域綁定
* 環境變數經 `.env` 管理

---

## 線上展示

本專案部署於 [Render](https://render.com)，並綁定自有網域 [hydraulink.press](https://hydraulink.press)（由 GoDaddy 註冊）。  
支援 HTTPS、短網址即時轉址、密碼驗證等功能，可直接線上試用。
