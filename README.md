# 奶泡器評論自動評分系統 (Frother Review Scoring System)

這個 Python 程式用於分析奶泡器產品的英文評論，並根據 6 個評分題型自動進行評分。

## 📋 功能說明

程式會分析每則英文評論，針對以下 6 個面向進行 1-7 分的評分：

| 評分題型 | 說明 |
|---------|------|
| 馬達效能 (Motor Performance) | 評估馬達動力、速度相關評價 |
| 電源類型 (Power Type) | 評估充電、電池相關評價 |
| 開關設計 (Switch Design) | 評估按鈕、開關設計相關評價 |
| 故障/壽命 (Failure/Durability) | 評估耐用性、故障相關評價 |
| 噪音 (Noise) | 評估噪音程度相關評價 |
| 中立意見 (Neutral Opinion) | 判斷是否為中立意見 |

### 評分標準

- **7分**: 極為滿意 (extremely satisfied)
- **6分**: 很滿意 (satisfied)
- **5分**: 稍微滿意 (slightly satisfied)
- **4分**: 中立/普通 (neutral)
- **3分**: 稍微不滿意 (slightly dissatisfied)
- **2分**: 不滿意 (dissatisfied)
- **1分**: 極不滿意 (extremely dissatisfied)
- **0 或空白**: 該題型未被提及

## 🛠️ 安裝指南

### 步驟 1: 安裝 Python

如果您的電腦尚未安裝 Python，請依照以下步驟：

#### Windows 用戶

1. 前往 [Python 官方網站](https://www.python.org/downloads/)
2. 點擊「Download Python 3.x.x」下載最新版本
3. 執行下載的安裝程式
4. **重要**: 勾選「Add Python to PATH」選項
5. 點擊「Install Now」完成安裝

#### Mac 用戶

1. 開啟終端機 (Terminal)
2. 輸入以下指令安裝 Homebrew（如尚未安裝）:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. 使用 Homebrew 安裝 Python:
   ```bash
   brew install python
   ```

### 步驟 2: 安裝必要套件

開啟命令提示字元 (Windows) 或終端機 (Mac/Linux)，輸入以下指令：

```bash
pip install pandas numpy
```

如果遇到權限問題，請嘗試：

```bash
pip install --user pandas numpy
```

## 🚀 使用方法

### 步驟 1: 準備檔案

確保以下檔案在同一個資料夾內：
- `frother_scoring.py` (評分程式)
- `奶泡器交易資料(luna) - 複製.csv` (輸入資料)

### 步驟 2: 執行程式

#### Windows 用戶

1. 開啟命令提示字元 (按 Win + R，輸入 `cmd`，按 Enter)
2. 切換到檔案所在的資料夾：
   ```bash
   cd 您的資料夾路徑
   ```
   例如：`cd C:\Users\YourName\Documents\frother_project`
3. 執行程式：
   ```bash
   python frother_scoring.py
   ```

#### Mac/Linux 用戶

1. 開啟終端機
2. 切換到檔案所在的資料夾：
   ```bash
   cd 您的資料夾路徑
   ```
3. 執行程式：
   ```bash
   python3 frother_scoring.py
   ```

### 步驟 3: 查看結果

程式執行完成後，會在同一資料夾產生 `奶泡器交易資料_已評分.csv` 檔案。

## 📁 檔案結構

```
專案資料夾/
├── frother_scoring.py              # 主程式
├── 奶泡器交易資料(luna) - 複製.csv   # 輸入檔案
├── 奶泡器交易資料_已評分.csv         # 輸出檔案（執行後產生）
└── README.md                        # 使用說明
```

## 📊 輸出格式

輸出的 CSV 檔案欄位順序如下：

```
comment | 馬達效能 | 電源類型 | 開關設計 | 故障/壽命 | 噪音 | 中立意見 | Analysis | ID | Q1_1 | Q1_2 | Q1_3 | Q1_4 | Q1_5 | Q1_6 | 電動滿意度總分 | 內容編碼表如下:
```

## ❓ 常見問題

### Q1: 出現「python 不是內部或外部命令」錯誤

**解決方法**: 
- 確認 Python 已正確安裝
- 確認安裝時有勾選「Add Python to PATH」
- 嘗試重新啟動命令提示字元

### Q2: 出現「No module named 'pandas'」錯誤

**解決方法**: 
執行以下指令安裝缺少的套件：
```bash
pip install pandas numpy
```

### Q3: 出現「找不到輸入檔案」錯誤

**解決方法**: 
- 確認 `奶泡器交易資料(luna) - 複製.csv` 檔案與程式在同一資料夾
- 確認檔案名稱完全正確（包括空格和副檔名）

### Q4: 輸出檔案中文亂碼

**解決方法**: 
- 使用 Excel 開啟時，選擇「UTF-8」編碼
- 或使用 Google 試算表開啟 CSV 檔案

### Q5: 如何查看程式是否正確執行？

程式執行時會顯示進度，最後會顯示評分統計摘要。如果看到「✅ 程式執行成功!」表示已完成。

## 📝 評分邏輯說明

### 馬達效能評分範例

| 評論內容 | 評分 | 原因 |
|---------|------|------|
| "This is a very powerful machine" | 7 | 極度正面 (very powerful) |
| "Fast and powerful" | 6 | 正面 (powerful) |
| "Weak motor, not impressed" | 2 | 負面 (weak) |

### 電源類型評分範例

| 評論內容 | 評分 | 原因 |
|---------|------|------|
| "Love the USB rechargeable feature" | 7 | 極度正面 |
| "Good battery life" | 6 | 正面 |
| "Battery dies quickly" | 2 | 負面 |

## 📞 技術支援

如有任何問題，請：
1. 確認已按照說明正確安裝 Python 和相關套件
2. 確認檔案名稱和路徑正確
3. 查看程式執行時的錯誤訊息

## 📄 授權

MIT License