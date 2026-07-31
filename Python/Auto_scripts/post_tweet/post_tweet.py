import os

import tweepy  # 导入 tweepy 库，用于与 Twitter API 进行交互

# 发布推文的函数
def post_tweet(api_key, api_secret, access_token, access_token_secret, message):
    """
    使用提供的凭据通过 Twitter API 发布推文。

    参数:
    api_key (str): Twitter API 的 API Key。
    api_secret (str): Twitter API 的 API Secret Key。
    access_token (str): 访问令牌（Access Token）。
    access_token_secret (str): 访问令牌密钥（Access Token Secret）。
    message (str): 要发布的推文内容。
    """
    # 使用 API Key 和 API Secret Key 进行 OAuth 认证
    auth = tweepy.OAuthHandler(api_key, api_secret)

    # 设置访问令牌和访问令牌密钥
    auth.set_access_token(access_token, access_token_secret)

    # 创建 Twitter API 对象
    api = tweepy.API(auth)

    # 使用 API 对象发布推文
    api.update_status(message)

# 使用示例
if __name__ == "__main__":
    # 凭据从环境变量读取，避免误提交到 Git 仓库。
    api_key = os.getenv('X_API_KEY')
    api_secret = os.getenv('X_API_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

    if not all((api_key, api_secret, access_token, access_token_secret)):
        raise SystemExit(
            '请先设置 X_API_KEY、X_API_SECRET、X_ACCESS_TOKEN '
            '和 X_ACCESS_TOKEN_SECRET 环境变量。'
        )

    # 要发布的推文内容
    message = 'Hello, Twitter!'

    # 调用 post_tweet 函数发布推文
    post_tweet(api_key, api_secret, access_token, access_token_secret, message)
