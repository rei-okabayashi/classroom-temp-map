# Git入門 — 企画者の素振りメニュー ＆ チーム用チートシート

- 対象：企画者（第1部）／チーム全員（第2部）
- 前提：`git` コマンドと VSCode のターミナルを使う（GitHub Desktopは使わない）
- 困ったときの合言葉：**まず `git status` を打つ。** 今どこにいて何が起きているかを教えてくれる。次の一手はだいたいそこから見える。

---

## 第1部：企画者の素振りメニュー（盆週必修・目安90分）

**対象：企画者本人。8/10〜8/14の準備週にひとりでやる。**

**ルール：この素振りの間はAIに手伝わせない（AI禁止）。** コマンドは全部自分の手で打つ。目的は「体で覚えること」。メンバーにDay 0で教える側になるので、まず自分がつまずいて、抜けて、を一通り経験しておく。

**練習用リポジトリはこのリポジトリの外に作る。**（`classroom-temp-map` の中にネストしたgitリポジトリを作らない）例：`C:\Users\nerun\git-practice`。練習が終わったら中身ごと削除してよい。

チェック欄は「これが確認できたらチェックを付けてよい」という基準。曖昧なまま進まない。

### ステップ0：練習場所を作る（目安5分）

- [ ] `classroom-temp-map` の外に練習用フォルダを作り、そこに移動する
  ```
  mkdir C:\Users\nerun\git-practice
  cd C:\Users\nerun\git-practice
  ```
  **チェック**：`cd` した先が `git-practice` になっている（プロンプトの表示で確認）。

### ステップ1：`git init`（目安5分）

- [ ] リポジトリを初期化する（`-b main` で最初のブランチ名をmainにする。素の `git init` だと環境によって `master` になり、後のステップの `git switch main` や `git push -u origin main` が失敗する）
  ```
  git init -b main
  git status
  ```
  **チェック**：`git status` の出力に「On branch main」「No commits yet」（または「まだコミットがありません」）が出る。`.git` フォルダができている。

### ステップ2：ファイル作成 → commit（目安10分）

- [ ] ファイルを1つ作って、最初のコミットをする
  ```
  echo test1 > memo.txt
  git add memo.txt
  git commit -m "最初のメモを追加"
  git log --oneline
  ```
  **チェック**：`git log --oneline` に自分のコミットが1件表示される。`git status` が「nothing to commit, working tree clean」に戻る。

### ステップ3：branch作成（目安5分）

- [ ] 作業用ブランチを作って切り替える
  ```
  git branch feature/color
  git switch feature/color
  git branch
  ```
  **チェック**：`git branch` の出力で `feature/color` の行に `*` が付いている（＝今そこにいる）。

### ステップ4：変更 → commit（目安10分）

- [ ] `feature/color` ブランチでファイルを編集してコミットする
  ```
  echo test2 >> memo.txt
  git add memo.txt
  git commit -m "2行目を追加"
  ```
  **チェック**：`git log --oneline` にコミットが2件になる。`git switch main` してから `git log --oneline` を見ると、mainはまだ1件のまま＝ブランチが分かれて独立していることが確認できる。作業後は `git switch feature/color` に戻しておく。

### ステップ5：merge（目安10分）

- [ ] `feature/color` の変更をmainに合流させる
  ```
  git switch main
  git merge feature/color
  git log --oneline --graph
  ```
  **チェック**：mainの `memo.txt` にも2行目が反映されている。`--graph` の出力で枝分かれ→合流の形が見える。

### ステップ6：わざとコンフリクトを起こす（目安10分）

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
  **チェック**：2つ目の `git merge branch-b` で `CONFLICT (content): Merge conflict in memo.txt` のようなメッセージが出る。`git status` に「both modified」と表示される。ここでわざと止まる（＝コンフリクトが起きた状態を自分の目で見る）のがこのステップのゴール。

### ステップ7：コンフリクト解消（目安15分）

- [ ] マーカーを手で直して解消する
  1. `memo.txt` をエディタで開く。中に次のようなマーカーがある。
     ```
     <<<<<<< HEAD
     A-version
     =======
     B-version
     >>>>>>> branch-b
     ```
  2. `<<<<<<<` `=======` `>>>>>>>` の3行と、要らない方の内容を消して、正しい内容だけを残す。
  3. 解消したら反映する。
     ```
     git add memo.txt
     git commit
     ```
     （コミットメッセージはデフォルトの「Merge branch 'branch-b'」のままでOK。エディタが開いたら保存して閉じる）

  **チェック**：`git status` が「nothing to commit, working tree clean」に戻る。`memo.txt` を開いてマーカー文字列（`<<<<<<<` など）が1文字も残っていないことを目で確認する。

### ステップ8：`git log` で履歴を眺める（目安5分）

- [ ] ここまでの流れをグラフで見る
  ```
  git log --oneline --graph --all
  ```
  **チェック**：ブランチが分かれて、コンフリクトを挟んで合流した形が線として見える。「このグラフの1行＝1コミット」という対応が自分の言葉で説明できる。

### ステップ9：`git revert` で取り消し体験（目安5分）

- [ ] 直前のコミットを打ち消す（履歴は消さない取り消し方）
  ```
  git revert HEAD
  git log --oneline
  ```
  **チェック**：新しいコミットが追加され、直前の変更内容が打ち消されている。`git log --oneline` には元のコミットも消えずに残っている（＝revertは「打ち消す記録を足す」であって「歴史を消す」ではない、と説明できる）。

### ステップ10：`git restore` で取り消し体験（目安5分）

- [ ] コミット前の変更を取り消す（履歴に残らない取り消し方）
  ```
  echo かきかけ >> memo.txt
  git status
  git restore memo.txt
  git status
  ```
  **チェック**：`restore` の前後で `git status` の表示が変わり、`restore` 後は編集前の内容に戻って「nothing to commit」になる。`git add` した後に取り消したいときは `git restore --staged memo.txt` を使うことも確認する。

### ステップ11：GitHub上でのPR練習（目安25分）

- [ ] 練習用のprivateリポジトリをGitHub上に作り、実際にPRを1本通す
  1. GitHubで新規リポジトリを作成する（Private、練習用の名前でOK。本番の `classroom-temp-map` とは別物）。
  2. ローカルの練習リポジトリを紐づけてpushする。
     ```
     git remote add origin <作ったリポジトリのURL>
     git push -u origin main
     ```
  3. 新しいブランチを切って何か変更し、pushする。
     ```
     git switch -c feature/practice-pr
     echo PR練習 >> memo.txt
     git add memo.txt
     git commit -m "PR練習用の変更"
     git push -u origin feature/practice-pr
     ```
  4. GitHubのWeb画面で「Compare & pull request」からPRを作成する。
  5. 自分でPRの内容を眺めてから「Merge pull request」でmergeする。
  6. ローカルに戻して取り込む。
     ```
     git switch main
     git pull
     ```

  **チェック**：GitHub上でPRがマージ済みになっている。ローカルで `git pull` した後、`main` ブランチに `feature/practice-pr` の変更が反映されている。練習が終わったらこのGitHubリポジトリは削除してよい。

---

## 第2部：チーム用チートシート

**対象：チーム全員。** このチームの運用は「feature branch → PR → 企画者レビュー → merge」。**mainへの直接pushは禁止。**

### 日常サイクル（コマンド一覧）

```
git switch main
git pull                              # 1. 最新のmainを取り込む

git switch -c feature/わかりやすい名前   # 2. 作業用ブランチを作る

# ここでファイルを編集する

git add <変更したファイル>              # 3. 変更をステージに乗せる
git commit -m "何をしたかを一言で"       # 4. コミット

git push -u origin feature/わかりやすい名前   # 5. GitHubへpush
```

→ GitHub上で「Compare & pull request」からPRを作成（PRテンプレートの3項目を自分の言葉で埋める：何をするコードか／動作確認したこと／AIを使った箇所）

→ 企画者にレビュー依頼 → 指摘があれば直してcommit・push（同じブランチに積むだけでPRに反映される）→ 企画者がmerge

```
git switch main
git pull                              # 6. mergeされた最新のmainを自分の手元にも取り込む
```

### 詰まり対処（落ち着いてこれを打つ）

#### コンフリクトが出た

落ち着いてこれを打つ：
```
git status
```
「both modified」と出ているファイルを開き、`<<<<<<<` `=======` `>>>>>>>` のマーカーを手で直して、要らない方を消す。直したら：
```
git add <直したファイル>
git commit
```
（第1部ステップ7と同じ手順。慌てず、マーカー文字列を消し切ることだけ確認する）

#### pushが拒否された（rejected / non-fast-forward）

落ち着いてこれを打つ：
```
git pull
```
これでリモートの変更が手元に取り込まれる。ここでコンフリクトが出たら「コンフリクトが出た」の手順へ。解消したらもう一度：
```
git push
```

#### mainに直接commitしてしまった

**まだpushしていない場合**、落ち着いてこれを打つ：
```
git branch feature/退避用の名前
git reset --hard origin/main
git switch feature/退避用の名前
```
1行目で今の変更を新しいブランチに逃がし、2行目でmainをリモートの状態に戻し、3行目で退避したブランチに移動して作業を続ける。

**すでにpush済みの場合**は自分で直そうとせず、企画者に相談する（mainの巻き戻しやforce pushが絡み、他の人にも影響するため）。

#### 変更を取り消したい

- まだ `git add` していない変更を捨てる：`git restore <ファイル>`
- `git add` 済みの変更をステージから外す（内容は残す）：`git restore --staged <ファイル>`
- commit済みの直前の変更を、履歴を残したまま打ち消す：`git revert HEAD`
- まだpushしていないcommitごと丸ごと消したい（注意：変更が本当に消える。pushしていないときだけ）：`git reset --hard HEAD~1`

#### HEADがdetachedになった

（「detached HEAD」＝ブランチの上ではなく、特定のコミットに直接乗ってしまっている状態。この状態でcommitすると、どのブランチにも属さない「迷子コミット」になりやすい）

落ち着いてこれを打つ：
```
git switch -
```
これで直前にいたブランチに戻れる。

もし迷子になる前に何か大事な変更をしていたら、先に退避してから戻る：
```
git switch -c 一時的な退避ブランチ名
```
（それから必要なら `git switch main` などで本来のブランチに合流させる）
