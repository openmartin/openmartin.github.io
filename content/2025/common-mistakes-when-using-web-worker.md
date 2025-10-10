Title: 使用 web worker 容易犯错的地方
Status: published
Date: 2025-10-09 20:00
Modified: 2025-10-09 20:00
Category: Web, Javascript
Tags: web, worker, javascript, typescript
Slug: common-mistakes-when-using-web-worker
Authors: Martin
Summary: 使用 web worker 容易犯错的地方

在浏览器中如果想把大量计算的任务放到新的线程中，可以使用 web worker，不影响用户交互的体验。

## web worker 的加载方式

如果不使用打包工具，在代码里可以这么写

```javascript
const worker = new Worker('/workers/worker.js');
```

主线程和 web worker 之间用 postMessage 来交互

```javascript
worker.postMessage(msg);

# 监听 work 发出的消息
worker.addEventListener("message", handleMessage);

# 在 worker 里面
self.postMessage(out)
```

### web worker 中的 base url

在 worker 里如果想要 fetch 一个网络资源，跟在网页上的行为差别很大，路径是相对于 worker 这个文件本身的。

```javascript
fetch('/static/dict.txt');
```

worker 的路径是 `/workers/worker.js`，上面 fetch 实际上的路径是 `/workers/static/dict.txt` 而不是像一般网页上的 `/static/dict.txt`。

如果对应的路径下有文件，是可以正常加载的。

### 以 Blob URL 方式加载 worker

还有一个坑是，如果使用了打包工具，比如在 Next.js 项目中，下面的加载方式实际上是使用 Blob URL 加载的

```javascript
const worker = new Worker(new URL("../workers/ocrWorker.ts", import.meta.url), { type: "module" });
```

如果在 worker 中有 fetch 代码，比如上面的 `fetch('/static/dict.txt')`，最后实际获取的是 `blob:/workers/static/dict.txt`，会出现 "Failed to parse URL" 错误。

这个时候需要写完整的 https 路径，不能只写一个 `/static/dict.txt`，比如 `https://example.com/static/dict.txt`

解决办法：可以读取环境变量，让打包的时候自动拼一下

```javascript
// 1. 优先使用环境变量（构建时注入）
if (typeof process !== 'undefined' && process.env?.NEXT_PUBLIC_SITE_URL) {
  baseUrl = process.env.NEXT_PUBLIC_SITE_URL;
  return baseUrl;
}
```

## web worker 中使用 Cache Storage

在 web worker 中也可以使用 [Cache Storage](https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage/open)，不过不在 window 对象下，要用 `self.caches`，也可以直接使用 `caches`
