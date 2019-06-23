# APIサーバー｜パスワード管理アプリ

## API

### Authentication
- **Login**
    - URL: POST http://localhost:4000/login
    - Request:
        - username: `ユーザー名`
        - password: `パスワード`
    - Response:
        - 200: `Logged in` (認証成功)
        - 400: `Authentication error` (認証失敗)
    - Usage:
        ```bash
        $ curl -c cookie -X POST -d 'username=ユーザー名' -d 'password=パスワード' http://localhost:4000/login
        ```
- **Logout**
    - URL: GET http://localhost:4000/logout
    - Response:
        - 200: `Logged out`
    - Usage:
        ```bash
        $ curl http://localhost:4000/logout
        ```

---

### Password Manager
- **Get Password Information**
    - URL: GET http://localhost:4000
    - Requirement:
        - Authentication
    - Response:
        - 200: パスワード情報
            ```json
            {
                "カテゴリー名": [
                    ["サービス名", "ユーザー名", "パスワード（暗号化済）", "備考（暗号化済）"],
                    ...
                ],
                ...
            }
            ```
        - 401: `Unauthenticated` (未認証)
    - Usage:
        ```bash
        $ curl -b cookie http://localhost:4000
        ```
- **Get Decrypted Password and Remarks**
    - URL: GET http://localhost:4000/password
    - Requirement:
        - Authentication
    - Request:
        - password: `暗号化されたパスワード`
        - remarks: `暗号化された備考`
    - Response:
        - 200: 平文パスワード, 備考
            ```json
            {
                "password": "平文パスワード",
                "remarks": "平文備考",
            }
            ```
        - 401: `Unauthenticated` (未認証)
    - Usage:
        ```bash
        $ curl -b cookie http://localhost:4000
        ```
