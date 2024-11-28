# Fantia Crawler / Fantia 媒体元数据抓取工具

[English](#english) | [中文](#中文)

## English

### Project Description
A metadata crawler for organizing Fantia videos for media servers like Jellyfin and Emby. This tool helps you manage and organize video metadata from Fantia posts.

### Important Notices
- **This project does NOT provide unauthorized video downloading**
- Some Fantia posts may require membership to access metadata

### Example

#### Before Organization

```ascii
/path/to/videos/****1.mp4
/path/to/videos/****2_part1.mp4
/path/to/videos/****2_part2.mp4
/path/to/videos/****3-Kita-Ikuyo.mov
/path/to/videos/Fantia-****4 Yamada Ryo-CD1.mp4
/path/to/videos/Fantia-****4 Yamada Ryo-CD2.mp4
```

#### After Organization

```ascii
/path/to/videos/****1
├── ****1.jpg
├── ****1.mp4
└── ****1.nfo

/path/to/videos/****2
├── ****2 part1.jpg
├── ****2 part1.mp4
├── ****2 part1.nfo
├── ****2 part2.jpg
├── ****2 part2.mp4
└── ****2 part2.nfo

/path/to/videos/****3
├── ****3.jpg
├── ****3.mov
└── ****3.nfo

/path/to/videos/****4
├── ****4 CD1.jpg
├── ****4 CD1.mp4
├── ****4 CD1.nfo
├── ****4 CD2.jpg
├── ****4 CD2.mp4
└── ****4 CD2.nfo
```

#### Media Library in Jellyfin

![](https://geelao-oss.oss-cn-hangzhou.aliyuncs.com/db/202411281114496.png?x-oss-process=style/jpeg)

![](https://geelao-oss.oss-cn-hangzhou.aliyuncs.com/db/202411281114234.png?x-oss-process=style/jpeg)

### Installation

```bash
pip install fantia-crawler
```

### Usage

```bash
fantia-crawler -e your_email@example.com -p your_password -d /path/to/video/directory
```

### Arguments
- `-e, --email`: Your Fantia account email
- `-p, --password`: Your Fantia account password
- `-d, --directory`: Directory to process videos (defaults to current directory)

### Usage Requirements
- Video filenames must include the Fantia post ID (from URL: https://fantia.jp/posts/xxxxxxx)
- Supported video formats: .mp4 and .mov
- Accompanying image files with the same name as the video will be automatically processed

### Login Process
- Manual login is required to avoid anti-crawler detection
- After logging in and returning to the Fantia homepage, press Enter in the command line to continue

## 中文

### 项目描述
用于整理Fantia视频元数据的爬虫工具，帮助您将视频轻松上架到Jellyfin、Emby等媒体服务器。

### 重要声明
- **本项目不提供未经授权的视频下载**
- 部分Fantia帖子可能需要成为会员才能获取元数据

### 安装

```bash
pip install fantia-crawler
```

### 使用方法

```bash
fantia-crawler -e 账号 -p 密码 -d 视频路径
```

### 参数说明
- `-e, --email`: Fantia账号邮箱
- `-p, --password`: Fantia账号密码
- `-d, --directory`: 视频处理目录（默认为当前目录）

### 使用要求
- 视频文件名必须包含Fantia帖子ID（来自URL: https://fantia.jp/posts/xxxxxxx）
- 支持的视频格式：.mp4 和 .mov
- 与视频文件同名的图像文件将被自动处理

### 登录流程

为避免反爬虫检测，需要手动登录。

在Selenium打开的页面成功登录并返回Fantia主页后，在命令行中按Enter继续