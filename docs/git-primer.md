# Git入門 — ひとり素振りメニュー ＆ チーム用チートシート

- 対象：チーム全員（第1部＝環境構築が終わった人からひとりで素振り／第2部＝チーム作業中に手元に置くチートシート）
- 前提：[setup-windows.md](setup-windows.md) の**5章まで**（Git for Windows と VSCode の導入、「名前とメールを設定する」）が終わっていること。名前とメールが未設定だと、最初のcommitが `Please tell me who you are` というエラーで止まります。学校PCでやる場合は、5章 手順4のプロキシ設定も済ませておいてください。
- ターミナルは **VSCodeのPowerShell** を使います（GitHub Desktopは使いません）。タブ名が「powershell」（プロンプトが `PS C:\...>` の形）であることを確認してください（setup-windows.md 5章 手順3と同じ確認です）。Git Bash や cmd では、この資料の `$HOME\git-practice` のような書き方が正しく動きません。
- 困ったときの合言葉：**まず `git status` を打ちましょう。** 今どこにいて何が起きているかを教えてくれます。次の一手はだいたいそこから見えてきます。

---

## 第1部：ひとり素振りメニュー（環境構築が終わった人から順に・目安90分）

**対象：チーム全員です。** 本番の `classroom-temp-map` での作業に入る前に、壊してもいい練習用リポジトリで、一連の操作をひとりで一通りやっておきます。

**ルール：この素振りの間はAIに手伝わせません（AI禁止）。** コマンドは全部自分の手で打ちます。目的は「体で覚えること」です。ここでつまずいて、自力で抜けて、を経験しておくと、本番のチーム作業で慌てなくなります。15分悩んでも抜けられないときは、AIではなく企画者に聞いてください。

**練習用リポジトリ（プロジェクト一式の保管場所。フォルダごと、変更履歴つきで置いておく場所です）は、このリポジトリの外に作ります。**（`classroom-temp-map` の中にネストしたgitリポジトリを作らないようにしてください）例：`C:\Users\自分のユーザー名\git-practice`（下のコマンドでは `$HOME` という省略記法で作ります）。練習が終わったら中身ごと削除してかまいません。

チェック欄は「これが確認できたらチェックを付けてよい」という基準です。曖昧なまま進まないようにしましょう。

### ステップ0：練習場所を作る（目安10分）

- [ ] ターミナルの文字コードを設定する（**ターミナルを開くたびに毎回**）
  ```
  $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
  ```
  （読み下し：`>` や `>>` でファイルに書き込むときの文字コードをUTF-8にする、というPowerShellの設定です。Windows標準のPowerShell 5.1では、これを設定しないと `>` がUTF-16という形式で書き込みます。UTF-16のファイルを、Gitはテキストではなくバイナリ（画像などと同じ「行単位で中身を比べられないデータ」）として扱うため、ステップ6〜7のコンフリクト練習が正しく動かなくなります。）

  **⚠ この設定は、いま開いているターミナルの中でだけ有効です。** 素振りの途中でターミナルを開き直したら（翌日に続きをやるときも）、必ずこの1行を打ち直してから再開してください。

  **チェック**：打ち間違いがなければ、何も表示されずに次のプロンプトが出ます（赤いエラーが出たら打ち直してください）。

- [ ] Gitが開くエディタをVSCodeにする（こちらは1回設定すれば以後ずっと有効です）
  ```
  git config --global core.editor "code --wait"
  ```
  （読み下し：Gitがコミットメッセージの入力を求める場面（ステップ7・9で出てきます）で、VSCodeを開くようにする設定です。設定しないままだと、Vim（ヴィム）という黒い画面のエディタが開きます。Vimは閉じ方が特殊で、知らないと固まってしまうため、先にVSCodeへ切り替えておきます。すでに設定済みの人が、もう一度打っても害はありません。）

  **チェック**：`git config --global core.editor` と打つと `code --wait` と表示されます。

- [ ] `classroom-temp-map` の外に練習用フォルダを作り、そこに移動する
  ```
  mkdir $HOME\git-practice
  cd $HOME\git-practice
  ```
  **チェック**：`cd` した先が `git-practice` になっていることを、プロンプトの表示で確認します（`$HOME` は自分のユーザーフォルダ（`C:\Users\ユーザー名`）を指す省略記法です）。

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
  **チェック**：`git log --oneline` に自分のコミットが1件表示されます。`git status` が「nothing to commit, working tree clean」に戻ります。つづけて `git show --stat HEAD` と打ち、`memo.txt | 1 +` のような行が出ることも見ておきます（「1行追加として記録された」という意味です）。ここがもし `memo.txt | Bin 0 -> 16 bytes` のように **`Bin`（バイナリ）** になっていたら、ステップ0の文字コード設定が効いていません。設定の1行を打ち直してから、次の3行でコミットを作り直してください（`--amend` は「直前のコミットを作り直す」という指定です）。
  ```
  echo test1 > memo.txt
  git add memo.txt
  git commit --amend -m "最初のメモを追加"
  ```

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
  **チェック**：mainの `memo.txt` にも2行目が反映されています。`git merge feature/color` の出力に `Fast-forward` と表示されています（合流までの間、main側では新しいコミットを作っていないため、Gitは合流用のコミットを作らず、mainの位置を `feature/color` の先頭まで進めるだけで済ませます。これを **fast-forward（早送り）** といいます。そのため `--graph` の表示はまだ一直線です。枝分かれ→合流の形が見えるのは、ステップ8まで進んでからです）。

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

  **⚠ もし出力に `warning: Cannot merge binary files` という行が混ざっていたら**、そのまま進んではいけません。ターミナルを開き直した後などに、ステップ0の文字コード設定が外れたまま `>` で書き込んだのが原因で、Gitがファイルをバイナリとみなしていて、ステップ7のマーカーを出せない状態です。こうなったら、練習リポジトリごと作り直すのがいちばん確実で速いです（練習用なので惜しくありません。2周目は驚くほど速く終わります）。
  ```
  cd $HOME
  Remove-Item -Recurse -Force $HOME\git-practice
  ```
  を実行してから、ステップ0（文字コード設定の打ち直しを含めて）からやり直してください（削除がエラーになったら、同じ `Remove-Item` をもう一度実行すれば消えます）。

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
     （読み下し：`<<<<<<< HEAD` から `=======` までが自分がいたブランチ側の内容、`=======` から `>>>>>>> branch-b` までが branch-b 側の内容です。マーカーが1つも見当たらない場合は先に進まず、ステップ6のチェックにある⚠の手順へ進んでください。）
  2. `<<<<<<<` `=======` `>>>>>>>` の3行と、要らない方の内容を消して、正しい内容だけを残します。**この練習では B-version の行を残してください**（＝最終的に `memo.txt` の中身が `B-version` の1行だけになるようにします）。どちらを残すかは本来その場の判断ですが、ここでA-versionを残すと「マージの前後で中身が変わらないマージコミット」ができてしまい、ステップ9の打ち消し練習が空振りになります（打ち消す変更が無い、と言われて何も起きません）。
  3. 解消したら反映します。
     ```
     git add memo.txt
     git commit
     ```
     （`git commit` と打つと、コミットメッセージの入力用にエディタが開きます。ステップ0の設定をしていれば、VSCodeに「Merge branch 'branch-b'」と書かれたタブが開くので、**何も書き換えずにそのタブを閉じれば**コミットが完了します（書き換えた場合は保存してから閉じます）。もし黒い画面のエディタ（Vim）が開いてしまったら：`Esc` を押してから `:wq` と打って `Enter` で、保存して閉じられます。）

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
  git revert -m 1 HEAD
  git log --oneline
  ```
  （ここでのHEAD＝直前のコミットは、ステップ7で作ったマージコミットです。マージコミットは「親」が2つあるため、どちら側を残すかを `-m 1`（1番目の親＝マージ先だったブランチ側）で指定しないとエラーになります。ふつうのコミットを打ち消すときは `git revert HEAD` だけで動きます。なお、revertでもコミットメッセージの入力用にエディタが開きます——ステップ7と同じく、何も書き換えずに閉じれば完了です）
  **チェック**：`Revert "Merge branch 'branch-b'"` という新しいコミットが追加され、`memo.txt` の中身が `A-version` に戻っています（＝ステップ7でマージ側から取り込んだB-versionが打ち消された、ということです）。`git log --oneline` には元のコミットも消えずに残っています（＝revertは「打ち消す記録を足す」ことであって「歴史を消す」ことではない、と自分の言葉で説明できれば十分です）。

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
  1. GitHub（書いたプログラムの変更履歴を記録・共有できるWebサービス）で新規リポジトリを作成します（Privateで、練習用の名前でOKです。本番の `classroom-temp-map` とは別物です）。**作成画面の「Add a README file」などの初期化オプションには何もチェックを入れず、空のまま作ってください。** チェックを入れるとGitHub側に先にコミットが1つでき、次の `git push -u origin main` が `! [rejected]` で失敗します（入れてしまった場合は、そのリポジトリの Settings → 最下部の Danger Zone → 「Delete this repository」で削除して、空で作り直すのが早いです）。
  2. ローカルの練習リポジトリを紐づけてpush（プッシュ。自分のPCでの記録をGitHub側に送って反映すること）します。
     ```
     git remote add origin <作ったリポジトリのURL>
     git push -u origin main
     ```
     （読み下し：`origin` は、clone元のGitHub上のリポジトリに自動で付く呼び名です。今回はcloneせず手元から紐づけるので、`git remote add` で自分で付けています。この素振りが自分の初めてのpushになる場合は、一度だけブラウザが開いてGitHubへのサインインと許可を求められます。setup-windows.md 5章「初回pushでは認証画面が出る（予告）」のとおり進めれば大丈夫です。）
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
これでリモート（＝GitHub側に置いてあるリポジトリ）の変更が手元に取り込まれます。このとき、取り込みを記録するマージコミットのメッセージ入力用にエディタが開くことがあります。第1部ステップ7と同じく、何も書き換えずに閉じればOKです。ここでコンフリクトが出たら「コンフリクトが出た」の手順に進んでください。解消したらもう一度：
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
- commit済みの直前の変更を、履歴を残したまま打ち消したいときは：`git revert HEAD`（直前がPRのマージコミットのときは `git revert -m 1 HEAD`。マージコミットは親が2つあるため、`-m 1`＝main側を残す指定が必要です。revertではコミットメッセージの入力用にエディタが開くので、何も書き換えずに閉じれば完了します）
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
