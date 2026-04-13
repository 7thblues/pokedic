# Ruby/Sapphire Notes 배포 절차

이 폴더는 정적 HTML/CSS/JS 공략 페이지입니다. GitHub Pages에 올리면 무료로 공유할 수 있습니다.

## 현재 상태

- 진입점: `index.html`
- 도감: `hoenn-pokedex-checklist.html`
- 기술표: `ruby-sapphire-move-guide.html`
- 정적 배포용: `.nojekyll` 포함
- 체크 상태: 브라우저 `localStorage`에 저장됨. GitHub에 올라가는 HTML 파일에는 개인 체크 상태가 포함되지 않음.

## 추천 배포 방식: GitHub Pages

GitHub 로그인은 필요합니다. 다만 이 Mac에 GitHub CLI가 없어도 브라우저에서 업로드할 수 있습니다.

### 1. GitHub에서 저장소 만들기

1. GitHub에 로그인합니다.
2. 새 저장소를 만듭니다.
3. 저장소 이름 예시: `ruby-sapphire-notes`
4. 공개 공유 목적이면 `Public`을 선택합니다.
5. README 자동 생성은 꺼도 됩니다. 이 폴더에 이미 `README.md`가 있습니다.

### 2. 이 폴더를 Git 저장소로 만들고 업로드

터미널에서 아래 명령을 실행합니다. `YOUR_GITHUB_ID`는 본인 GitHub 아이디로 바꿉니다.

```sh
cd /Users/beomsuk/pokemon/ruby-sapphire-notes
git init
git add .
git commit -m "Publish Ruby/Sapphire notes"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_ID/ruby-sapphire-notes.git
git push -u origin main
```

GitHub 로그인이 필요하다는 메시지가 나오면 브라우저 로그인 또는 Personal Access Token 인증을 진행합니다.

### 3. GitHub Pages 켜기

1. GitHub 저장소 페이지로 이동합니다.
2. `Settings` -> `Pages`로 갑니다.
3. `Build and deployment`에서 `Deploy from a branch`를 선택합니다.
4. Branch는 `main`, 폴더는 `/ (root)`를 선택합니다.
5. 저장합니다.

배포가 끝나면 대개 아래 주소로 접근할 수 있습니다.

```text
https://YOUR_GITHUB_ID.github.io/ruby-sapphire-notes/
```

## 이후 수정해서 다시 배포

```sh
cd /Users/beomsuk/pokemon/ruby-sapphire-notes
git add .
git commit -m "Update notes"
git push
```

GitHub Pages는 push 후 자동으로 다시 배포됩니다.

## 주의

- `file://`에서 쓰던 체크 상태와 `https://...github.io/...`에서 쓰는 체크 상태는 서로 공유되지 않습니다.
- 체크 상태는 방문자별 브라우저에 저장됩니다.
- 공개 저장소에 올리면 HTML 안의 공략 데이터는 누구나 볼 수 있습니다.
