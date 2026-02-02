// 心动积分 PWA Service Worker
// 版本号 - 更新时修改此版本号以触发更新
const CACHE_VERSION = 'v2.1.1';
const CACHE_NAME = `heart-rhythm-${CACHE_VERSION}`;

// 需要缓存的静态资源
const STATIC_CACHE_URLS = [
  '/',
  '/login',
  '/static/manifest.json',
  // Bootstrap CSS
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  // Bootstrap Icons
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
  // Google Fonts
  'https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@300;400;500;700&display=swap',
  // Bootstrap JS
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
];

// 动态缓存的资源（页面和图片）
const DYNAMIC_CACHE_NAME = `heart-rhythm-dynamic-${CACHE_VERSION}`;
const MAX_DYNAMIC_CACHE_SIZE = 50; // 最多缓存50个动态资源

// API请求不缓存，始终从网络获取
const API_URLS = ['/api/'];

// 清理旧缓存
async function cleanupOldCaches(currentCaches) {
  const cacheNames = await caches.keys();
  return Promise.all(
    cacheNames
      .filter(cacheName => !currentCaches.includes(cacheName))
      .map(cacheName => {
        console.log('[Service Worker] 删除旧缓存:', cacheName);
        return caches.delete(cacheName);
      })
  );
}

// 限制动态缓存大小
async function limitCacheSize(cacheName, maxSize) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  if (keys.length > maxSize) {
    // 删除最旧的缓存项
    await cache.delete(keys[0]);
    await limitCacheSize(cacheName, maxSize);
  }
}

// 安装事件 - 缓存静态资源
self.addEventListener('install', (event) => {
  console.log('[Service Worker] 安装中...', CACHE_VERSION);

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] 缓存静态资源');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        console.log('[Service Worker] 安装完成');
        // 强制激活新的Service Worker
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[Service Worker] 安装失败:', error);
      })
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] 激活中...', CACHE_VERSION);

  event.waitUntil(
    (async () => {
      // 清理旧缓存
      await cleanupOldCaches([CACHE_NAME, DYNAMIC_CACHE_NAME]);
      console.log('[Service Worker] 激活完成');
      // 立即控制所有页面
      return self.clients.claim();
    })()
  );
});

// 请求拦截 - 缓存策略
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API请求：网络优先策略
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // API请求成功，直接返回
          return response;
        })
        .catch((error) => {
          console.error('[Service Worker] API请求失败:', error);
          // 返回离线提示
          return new Response(
            JSON.stringify({
              error: '网络连接失败',
              message: '请检查网络连接后重试'
            }),
            {
              status: 503,
              headers: { 'Content-Type': 'application/json' }
            }
          );
        })
    );
    return;
  }

  // HTML页面请求：网络优先，失败时返回缓存
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          // 缓存新获取的页面
          const responseToCache = response.clone();
          caches.open(DYNAMIC_CACHE_NAME).then(cache => {
            cache.put(request, responseToCache);
          });
          return response;
        })
        .catch(() => {
          // 网络失败，返回缓存
          return caches.match(request);
        })
    );
    return;
  }

  // 静态资源：缓存优先策略（图片、字体等）
  if (request.destination === 'image' || request.destination === 'font') {
    event.respondWith(
      caches.match(request)
        .then(cached => {
          if (cached) {
            return cached;
          }
          return fetch(request)
            .then(response => {
              if (!response || response.status !== 200) {
                return response;
              }
              // 缓存图片和字体
              const responseToCache = response.clone();
              caches.open(DYNAMIC_CACHE_NAME).then(cache => {
                cache.put(request, responseToCache);
                limitCacheSize(DYNAMIC_CACHE_NAME, MAX_DYNAMIC_CACHE_SIZE);
              });
              return response;
            });
        })
    );
    return;
  }

  // 其他静态资源：缓存优先策略
  event.respondWith(
    caches.match(request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // 缓存命中，返回缓存
          console.log('[Service Worker] 缓存命中:', request.url);
          return cachedResponse;
        }

        // 缓存未命中，从网络获取
        return fetch(request)
          .then((response) => {
            // 检查响应是否有效
            if (!response || response.status !== 200 || response.type === 'error') {
              return response;
            }

            // 克隆响应（响应流只能读取一次）
            const responseToCache = response.clone();

            // 缓存新资源
            caches.open(CACHE_NAME)
              .then((cache) => {
                // 只缓存GET请求
                if (request.method === 'GET') {
                  cache.put(request, responseToCache);
                }
              });

            return response;
          })
          .catch((error) => {
            console.error('[Service Worker] 网络请求失败:', error);

            // 返回离线页面（如果有的话）
            if (request.destination === 'document') {
              return caches.match('/');
            }

            return new Response('离线状态', {
              status: 503,
              statusText: 'Service Unavailable'
            });
          });
      })
  );
});

// 后台同步（可选功能）
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] 后台同步:', event.tag);

  if (event.tag === 'sync-points') {
    event.waitUntil(
      // 这里可以实现离线数据同步逻辑
      Promise.resolve()
    );
  }
});

// 推送通知（可选功能）
self.addEventListener('push', (event) => {
  console.log('[Service Worker] 收到推送通知');

  const options = {
    body: event.data ? event.data.text() : '你有新的消息',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: '查看详情'
      },
      {
        action: 'close',
        title: '关闭'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('心动积分', options)
  );
});

// 通知点击事件
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] 通知被点击:', event.action);

  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// 消息事件 - 与页面通信
self.addEventListener('message', (event) => {
  console.log('[Service Worker] 收到消息:', event.data);

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
