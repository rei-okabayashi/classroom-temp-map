# Git入門 — 企画者の素振りメニュー ＆ チーム用チートシート

- 対象：企画者（第1部）／チーム全員（第2部）
- 前提：`git` コマンドと VSCode のターミナルを使います（GitHub Desktopは使いません）。
- 困ったときの合言葉：**まず `git status` を打ちましょう。** 今どこにいて何が起きているかを教えてくれます。次の一手はだいたいそこから見えてきます。

---

## 第1部：企画者の素振りメニュー（盆週必修・目安90分）

**対象：企画者本人です。8/10〜8/14の準備週にひとりでやります。**

**ルール：この素振りの間はAIに手伝わせません（AI禁止）。** コマンドは全部自分の手で打ちます。目的は「体で覚えること」です。メンバーにDay 0で教える側になるので、まず自分がつまずいて、抜けて、を一通り経験しておきましょう。

**練習用リポジトリ（プロジェクト一式の保管場所。フォルダごと、変更履歴つきで置いておく場所です）は、このリポジトリの外に作ります。**（`classroom-temp-map` の中にネストしたgitリポジトリを作らないようにしてください）例：`C:\Users\nerun\git-practice`。練習が終わったら中身ごと削除してかまいません。

チェック欄は「これが確認できたらチェックを付けてよい」という基準です。曖昧なまま進まないようにしましょう。

### ステップ0：練習場所を作る（目安5分）

- [ ] `classroom-temp-map` の外に練習用フォルダを作り、そこに移動する
  ```
  mkdir C:\Users\nerun\git-practice
  cd C:\Users\nerun\git-practice
  ```
  **チェック**：`cd` した先が `git-practice` になっていることを、プロンプトの表示で確認します。

### ステップ1：`git init`（目安5分）

- [ ] リポジトリを初期化する（`-b main` は、最初のブランチ名を main にする指定です。ブランチとは、本体に影響を与えずに作業するための、枝分かれした作業用コピーのことです。素の `git init` だと環境によって `master` になり、後のステップの `git switch main` や `git push -u origin main` が失敗します）
  ```
  git init -b main
  git status
  ```
  **チェック**：`git status` の出力に「On branch main」「No commits yet」（または「まだコミットがありません」）が出ます。`.git` フォルダができています。

### ステップ2：ファイル作成 → commit（目安10分）

- [ ] ファイルを1つ作って、最初のコミット（変更内容の記録。ゲームのセーブポイントのようなものです）をする
  ```
  echo test1 > memo.txt
  git add memo.txt
  git commit -m "最初のメモを追加"
  git log --oneline
  ```
  **チェック**：`git log --oneline` に自分のコミットが1件表示されます。`git status` が「nothing to commit, working tree clean」に戻ります。

### ステップ3：branch作成（目安5分）

- [ ] 作業用ブランチを作って切り替える
  ```
  git branch feature/color
  git switch feature/color
  git branch
  ```
  **チェック**：`git branch` の出力で `feature/color` の行に `*` が付いています（＝今そこにいるという意味です）。

### ステップ4：変更 → commit（目安10分）

- [ ] `feature/color` ブランチでファイルを編集してコミットする
  ```
  echo test2 >> memo.txt
  git add memo.txt
  git commit -m "2行目を追加"
  ```
  **チェック**：`git log --oneline` にコミットが2件になります。`git switch main` してから `git log --oneline` を見ると、mainはまだ1件のままです。つまりブランチが分かれて独立していることが確認できます。作業後は `git switch feature/color` に戻しておきましょう。

### ステップ5：merge（目安10分）

- [ ] `feature/color` の変更をmainに合流させる
  ```
  git switch main
  git merge feature/color
  git log --oneline --graph
  ```
  **チェック**：mainの `memo.txt` にも2行目が反映されています。`--graph` の出力で枝分かれ→合流の形が見えます。

### ステップ6：わざとコンフリクトを起こす（目安10分）

**コンフリクト**とは、同じ行を2人が別々に直したためGitが自動では合流できなくなった状態のことです。このステップでは、わざとコンフリクトを起こして直し方を覚えます。

- [ ] 2つのブランチで同じ行を別の内容に書き換えて、両方をmainにmergeする
  ```
  git switch -c branch-a
  echo A-version > memo.txt
  git add memo.txt
  git commit -m "branch-aでmemo.txtをA版に"

  git switch main
  git switch -c branch-b
  echo B-version > memo.txt
  git add memo.txt
  git commit -m "branch-bでmemo.txtをB版に"

  git switch main
  git merge branch-a
  git merge branch-b
  ```
  **チェック**：2つ目の `git merge branch-b` で `CONFLICT (content): Merge conflict in memo.txt` のようなメッセージが出ます。`git status` に「both modified」と表示されます。ここでわざと止まる（＝コンフリクトが起きた状態を自分の目で見る）のがこのステップのゴールです。

### ステップ7：コンフリクト解消（目安15分）

- [ ] マーカーを手で直して解消する
  1. `memo.txt` をエディタで開きます。中に次のようなマーカーがあります。
     ```
     <<<<<<< HEAD
     A-version
     =======
     B-version
     >>>>>>> branch-b
     ```
     （読み下し：`<<<<<<< HEAD` から `=======` までが自分がいたブランチ側の内容、`=======` から `>>>>>>> branch-b` までが branch-b 側の内容です。）
  2. `<<<<<<<` `=======` `>>>>>>>` の3行と、要らない方の内容を消して、正しい内容だけを残します。
  3. 解消したら反映します。
     ```
     git add memo.txt
     git commit
     ```
     （コミットメッセージはデフォルトの「Merge branch 'branch-b'」のままでOKです。エディタが開いたら保存して閉じてください）

  **チェック**：`git status` が「nothing to commit, working tree clean」に戻ります。`memo.txt` を開いてマーカー文字列（`<<<<<<<` など）が1文字も残っていないことを目で確認します。

### ステップ8：`git log` で履歴を眺める（目安5分）

- [ ] ここまでの流れをグラフで見る
  ```
  git log --oneline --graph --all
  ```
  **チェック**：ブランチが分かれて、コンフリクトを挟んで合流した形が線として見えます。「このグラフの1行＝1コミット」という対応が自分の言葉で説明できます。

### ステップ9：`git revert` で取り消し体験（目安5分）

- [ ] 直前のコミットを打ち消す（履歴は消さない取り消し方）
  ```
  git revert HEAD
  git log --oneline
  ```
  **チェック**：新しいコミットが追加され、直前の変更内容が打ち消されています。`git log --oneline` には元のコミットも消えずに残っています（＝revertは「打ち消す記録を足す」ことであって「歴史を消す」ことではない、と自分の言葉で説明できれば十分です）。

### ステップ10：`git restore` で取り消し体験（目安5分）

- [ ] コミット前の変更を取り消す（履歴に残らない取り消し方）
  ```
  echo かきかけ >> memo.txt
  git status
  git restore memo.txt
  git status
  ```
  **チェック**：`restore` の前後で `git status` の表示が変わり、`restore` 後は編集前の内容に戻って「nothing to commit」になります。`git add` した後に取り消したいときは `git restore --staged memo.txt` を使うことも確認しておきましょう。

### ステップ11：GitHub上でのPR練習（目安25分）

- [ ] 練習用のprivateリポジトリをGitHub上に作り、実際にPRを1本通す
  1. GitHub（書いたプログラムの変更履歴を記録・共有できるWebサービス）で新規リポジトリを作成します（Privateで、練習用の名前でOKです。本番の `classroom-temp-map` とは別物です）。
  2. ローカルの練習リポジトリを紐づけてpush（プッシュ。自分のPCでの記録をGitHub側に送って反映すること）します。
     ```
     git remote add origin <作ったリポジトリのURL>
     git push -u origin main
     ```
     （読み下し：`origin` は、clone元のGitHub上のリポジトリに自動で付く呼び名です。）
  3. 新しいブランチを切って何か変更し、pushします。
     ```
     git switch -c feature/practice-pr
     echo PR練習 >> memo.txt
     git add memo.txt
     git commit -m "PR練習用の変更"
     git push -u origin feature/practice-pr
     ```
  4. GitHubのWeb画面で「Compare & pull request」からPR（Pull Request。「この変更を本体に取り込んでください」という提案です。チームの誰かが確認してから取り込みます）を作成します。
  5. 自分でPRの内容を眺めてから「Merge pull request」でmerge（マージ。提案された変更を本体に取り込むこと）します。
  6. ローカルに戻して取り込みます。
     ```
     git switch main
     git pull
     ```

  **チェック**：GitHub上でPRがマージ済みになっています。ローカルで `git pull` した後、`main` ブランチに `feature/practice-pr` の変更が反映されています。練習が終わったらこのGitHubリポジトリは削除してかまいません。

---

## 第2部：チーム用チートシート

**対象：チーム全員。** このチームの運用は「feature branch → PR → 企画者レビュー → merge」です。**mainへの直接pushは禁止です。**

**用語のおさらい**

- ブランチ＝本体（main）に影響を与えずに作業するための、枝分かれした作業用コピー
- コミット＝変更内容の記録（ゲームのセーブポイントのようなもの）
- push（プッシュ）＝自分のPCでの記録をGitHub側に送って反映すること
- PR（Pull Request）＝「この変更を本体に取り込んでください」という提案。チームの誰かが確認してから取り込みます
- マージ＝提案された変更を本体に取り込むこと

### 日常サイクル（コマンド一覧）

**ステージ**とは、次のコミットに入れる変更を載せておく準備台のことです（`git add` で載せます）。

```
git switch main
git pull                              # 1. 最新のmainを取り込む

git switch -c feature/わかりやすい名前   # 2. 作業用ブランチを作る

# ここでファイルを編集する

git add <変更したファイル>              # 3. 変更をステージに乗せる
git commit -m "何をしたかを一言で"       # 4. コミット

git push -u origin feature/わかりやすい名前   # 5. GitHubへpush
```

→ GitHub上で「Compare & pull request」からPRを作成します（PRテンプレートの3項目を自分の言葉で埋めます：何をするコードか／動作確認したこと／AIを使った箇所）。

→ 企画者にレビューを依頼します → 指摘があれば直してcommit・pushします（同じブランチに積むだけでPRに反映されます）→ 企画者がmergeします

```
git switch main
git pull                              # 6. mergeされた最新のmainを自分の手元にも取り込む
```

### 詰まり対処（落ち着いてこれを打つ）

#### コンフリクトが出た

落ち着いてこれを打ちましょう：
```
git status
```
「both modified」と出ているファイルを開き、`<<<<<<<` `=======` `>>>>>>>` のマーカーを手で直して、要らない方を消します。直したら：
```
git add <直したファイル>
git commit
```
（第1部ステップ7と同じ手順です。慌てず、マーカー文字列を消し切ることだけ確認しましょう）

#### pushが拒否された（rejected / non-fast-forward）

落ち着いてこれを打ちましょう：
```
git pull
```
これでリモート（＝GitHub側に置いてあるリポジトリ）の変更が手元に取り込まれます。ここでコンフリクトが出たら「コンフリクトが出た」の手順に進んでください。解消したらもう一度：
```
git push
```

#### mainに直接commitしてしまった

**まだpushしていない場合**、落ち着いてこれを打ちましょう：
```
git branch feature/退避用の名前
git reset --hard origin/main
git switch feature/退避用の名前
```
1行目で今の変更を新しいブランチに逃がします。2行目でmainをリモートの状態に戻します。3行目で退避したブランチに移動して作業を続けます。

**すでにpush済みの場合**は自分で直そうとせず、企画者に相談してください（mainの巻き戻しや、履歴を強制的に上書きする「force push」が絡み、他の人にも影響するためです）。

#### 変更を取り消したい

- まだ `git add` していない変更を捨てたいときは：`git restore <ファイル>`
- `git add` 済みの変更をステージから外したいとき（内容は残ります）：`git restore --staged <ファイル>`
- commit済みの直前の変更を、履歴を残したまま打ち消したいときは：`git revert HEAD`
- まだpushしていないcommitごと丸ごと消したいとき（注意：変更が本当に消えます。pushしていないときだけ）：`git reset --hard HEAD~1`

#### HEADがdetachedになった

（「detached HEAD」とは、ブランチの上ではなく特定のコミットに直接乗ってしまっている状態のことです。この状態でcommitすると、どのブランチにも属さない「迷子コミット」になりやすいです）

落ち着いてこれを打ちましょう：
```
git switch -
```
これで直前にいたブランチに戻れます。

もし迷子になる前に何か大事な変更をしていたら、先に退避してから戻りましょう：
```
git switch -c 一時的な退避ブランチ名
```
（それから必要なら `git switch main` などで本来のブランチに合流させます）
