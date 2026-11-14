// Prototype service worker: network only, enables "install as app". Caches nothing.
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>self.clients.claim());
self.addEventListener('fetch',()=>{});
