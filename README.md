# Data to Dashboard Skill｜從資料到動態儀表板

這是一個給 Codex 使用的 skill。它會讀取你電腦資料夾中的表格資料，協助建立 Google 試算表與 Google Apps Script 動態儀表板，最後核對網頁上的數字是否真的和原始資料一致。

你不需要先懂程式。skill 會先掃描環境、告訴你還少哪些工具或網址，並在需要你親自登入或授權時清楚說明下一步。

## 它能幫你做什麼？

1. 找出資料夾內的 CSV、TSV、JSON、XLSX、XLS、ODS 等表格資料。
2. 檢查檔案欄位、筆數、雜湊值，以及電腦是否具備建立儀表板所需工具。
3. 提醒你缺少的項目，例如 Node.js、Clasp、Google 試算表網址或 Apps Script 專案網址。
4. 先確認資料定義，再建立 KPI 指標、篩選器、圖表及月報工作表。
5. 將程式推送到你指定的 Google Apps Script 專案，建立更新機制並部署網頁。
6. 開啟正式 `/exec` 儀表板網址，比對本機資料、試算表資料和網頁數字。
7. 做一次可還原的資料更新測試，確認更新與還原都正常。

## 開始前要準備什麼？

| 項目 | 為什麼需要 | 你要做什麼 |
| --- | --- | --- |
| 資料資料夾 | 儀表板的來源 | 準備 CSV、Excel、ODS、JSON 等資料檔。請先知道哪些是正式資料，哪些只是範例或測試檔。 |
| Google 帳號 | 建立與管理試算表、Apps Script | 使用有權限編輯目標專案與試算表的帳號。 |
| Apps Script 專案網址 | 決定程式要部署到哪個專案 | 網址格式通常含有 `/projects/` 和 `/edit`。 |
| Google 試算表網址 | 放置來源資料與產出月報 | 可提供現有試算表，或在任務中授權建立新的試算表。 |
| Python 3 | 執行環境掃描 | 多數 macOS 環境已具備。skill 的掃描程式只使用 Python 內建功能。 |
| Node.js、npm、Clasp | 將程式同步到 Apps Script | skill 會檢查是否缺少，並提供安裝指引。 |

## 安裝 skill

### 方法一：從 GitHub 安裝（建議）

在終端機執行以下指令：

```bash
git clone https://github.com/FW1201/data-to-dashboard-skill.git \
  ~/.codex/skills/data-to-dashboard-skill
```

完成後，skill 會位於：

```text
~/.codex/skills/data-to-dashboard-skill/
```

### 方法二：下載後手動放入資料夾

1. 從 [GitHub 儲存庫](https://github.com/FW1201/data-to-dashboard-skill) 下載或複製整個資料夾。
2. 將整個資料夾放進 `~/.codex/skills/`。
3. 確認資料夾名稱是 `data-to-dashboard-skill`。

完成後的結構應該如下：

```text
~/.codex/skills/data-to-dashboard-skill/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── references/
└── scripts/scan_environment.py
```

### 確認安裝成功

在終端機執行：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  ~/.codex/skills/data-to-dashboard-skill
```

如果看到以下結果，表示結構正確：

```text
Skill is valid!
```

若 Codex 沒有立刻顯示新名稱，重新整理技能清單或重新開啟 Codex。之後可以輸入 `$data-to-dashboard-skill` 使用它。

## 第一次使用：先掃描環境

請將下列指令中的三個內容換成自己的路徑或網址：

```bash
python3 ~/.codex/skills/data-to-dashboard-skill/scripts/scan_environment.py \
  --folder /你的/資料夾/路徑 \
  --script-id 'https://script.google.com/u/0/home/projects/你的_SCRIPT_ID/edit' \
  --spreadsheet-id 'https://docs.google.com/spreadsheets/d/你的_SHEET_ID/edit'
```

不知道怎麼找網址時，可依照下表：

| 你需要的東西 | 從哪裡找 | 常見錯誤 |
| --- | --- | --- |
| Apps Script 專案網址／Script ID | 打開 Apps Script 編輯器，網址中的 `/projects/` 與 `/edit` 之間就是 Script ID。 | 不要提供 `AKfy...`；它通常是網頁部署 ID，不是程式專案 ID。 |
| 試算表網址／Sheet ID | 打開 Google 試算表，網址 `/d/` 後面的字串就是 Sheet ID。 | 不要拿其他專案的試算表網址來代替。 |
| 正式資料檔 | 你的專案資料夾。 | 不要把備份、範例或「追加測試」檔誤認為正式來源。 |

如果也要將這個通用 skill 發布到 GitHub，才加上 `--publish-github`：

```bash
python3 ~/.codex/skills/data-to-dashboard-skill/scripts/scan_environment.py \
  --folder /你的/資料夾/路徑 --publish-github
```

## 看懂掃描結果

掃描結果是 JSON 格式。你不需要自己修程式，只要看這四個區塊：

| 欄位 | 代表什麼 | 你接下來要做什麼 |
| --- | --- | --- |
| `files` | 找到的資料檔、欄位、筆數與雜湊值 | 確認哪些檔案是正式來源。 |
| `missing_or_next_actions` | 缺少的工具、網址或資料 | 逐項補齊，不要猜測 ID。 |
| `installation_and_access_guidance` | 安裝、登入與授權的操作說明 | 只做目前適用的步驟，完成後再重新掃描。 |
| `remote_checks_still_required` | 本機掃描無法確認的 Google 權限 | 在指定的 Google 帳號中確認後才能部署。 |

## 安裝與登入引導

skill 會依你的電腦狀態提出需要的步驟。常見情況如下：

### 1. 找不到 Node.js 或 npm

請到 [Node.js 官方網站](https://nodejs.org/) 安裝目前的 LTS 版本，或依組織規範使用指定的套件管理工具。安裝完後重新執行環境掃描。

### 2. 找不到 Clasp

Clasp 是把本機 Apps Script 程式同步到 Google 的工具。先確認 Node.js 可用，再執行：

```bash
npm install --global @google/clasp
```

完成後重新掃描；結果中應該會顯示 Clasp 版本。

### 3. Clasp 尚未登入 Google

執行：

```bash
clasp login
```

瀏覽器會要求登入 Google。請選擇同時具有下列權限的帳號：

- 可編輯目標 Apps Script 專案；
- 可編輯目標 Google 試算表；
- 可建立或更新網頁部署。

不要把登入產生的 `.clasprc.json` 放進專案資料夾或上傳到 GitHub。

### 4. Google 要求授權

首次執行時，Google 可能要求允許程式讀寫指定試算表、執行初始化、建立更新觸發器與顯示網頁儀表板。請先閱讀權限範圍，再依需求允許。

若 Google 顯示「未驗證應用程式」警告，請由你本人在瀏覽器確認專案名稱、登入帳號和權限後再完成允許。這是 Google 的安全步驟，skill 不會自動跨過它。

### 5. 要發佈到 GitHub

只有在你要公開「通用 skill」時才需要 GitHub CLI。可從 [GitHub CLI](https://cli.github.com/) 安裝，接著執行：

```bash
gh auth login
```

發布前請確認公開內容不含任何資料檔、試算表 ID、Script ID、部署網址、登入資訊、截圖或個人路徑。

## 使用流程

整個流程會依下列順序進行：

1. **確認資料來源**：指出哪些檔案是真正要上儀表板的資料，並說明每個指標的意義、單位、日期範圍與缺值處理方式。
2. **確認目標 Google 專案**：提供 Apps Script 編輯器網址與試算表網址；skill 會先核對 ID，避免推到錯的專案。
3. **建立儀表板**：保留既有來源工作表，建立產生用的月報、圖表、篩選器與更新機制。
4. **部署網頁**：完成初始化後建立或更新網頁應用程式，並以正式 `/exec` 網址作為交付成果。
5. **比對驗收**：比對本機資料、試算表資料與網頁數字，至少驗證預設篩選與另一種篩選條件。
6. **更新測試與還原**：暫時調整一個安全的來源儲存格、確認預期變化、還原原值，再確認所有來源表與本機資料一致。

## 資料更新會怎麼反映？

要先分清楚資料從哪裡改：

| 你改的位置 | 是否會自動反映到儀表板 | 備註 |
| --- | --- | --- |
| Google 試算表來源工作表 | 可以設定為觸發重新計算 | 取決於已安裝的觸發器。 |
| 外部 API、匯入資料或公式變化 | 可用排程定期檢查 | Google 排程不是精確到秒的服務。 |
| 本機 CSV／Excel 檔 | 不會自動上傳 | 需要額外設計同步或匯入流程。 |

## 安全的更新測試方式

測試線上更新前，先記錄：

- 工作表名稱與確切 A1 儲存格位置；
- 該筆資料的唯一編號；
- 原始值、暫時值與還原值；
- 預期會改變的儀表板數字。

盡量使用精準的範圍更新或連接器操作，不要在切換試算表分頁後直接輸入。因為游標可能落在別的工作表，造成誤改。

有些 API 更新不會觸發 Apps Script 的 `onEdit`。遇到這種情況，請執行排程刷新或重建月報後再判斷網頁是否有更新。測試結束必須還原原值，並再次比對遠端來源表與本機資料。

## 完成後你會拿到什麼？

- 正式的 `/exec` 儀表板網址；
- 來源 Google 試算表網址；
- 已驗證的 Apps Script ID；
- 更新頻率與觸發器行為；
- 本機與遠端資料的筆數、關鍵總計比對結果；
- 更新、還原測試的結果；
- 任何尚未驗證的限制，例如檢視者權限或外部匯入流程。

## 隱私與公開原則

公開 GitHub 儲存庫只能放通用 skill 內容，例如 `SKILL.md`、`README.md`、`agents/`、`references/`、`scripts/` 和授權檔。

請勿公開資料檔、憑證、`.clasprc.json`、畫面截圖、執行紀錄、個人電腦路徑、Google 試算表 ID、Apps Script ID 或部署網址。

本 skill 採用 MIT License。

