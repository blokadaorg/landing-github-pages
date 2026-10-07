// The homepage no longer uses a service worker. Browsers that registered the
// old precaching one fetch this file on their next visit: it deletes that
// worker's caches and unregisters itself. The open page is left alone, and
// the visit after that comes from the network. Keep this file published.
self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      // Workbox named its caches after the "landing" prefix.
      .then(keys => Promise.all(keys.filter(key => key.startsWith('landing-')).map(key => caches.delete(key))))
      .then(() => self.registration.unregister())
  );
});
