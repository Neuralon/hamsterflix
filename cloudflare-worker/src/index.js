export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const referer = request.headers.get('Referer') || request.headers.get('Origin') || '';
    
    // Default to the production domain, but allow localhost and the Pages *.hamsterflix.pages.dev preview URLs to pass through 
    const origin = request.headers.get('Origin') || 'https://hamsterflix.neuralon.ai';
    let allowedOrigin = 'https://hamsterflix.neuralon.ai';
    if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
      allowedOrigin = origin;
    } else if (origin.includes('.hamsterflix.pages.dev')) {
      allowedOrigin = origin;
    }
    
    // Allow options requests for CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': allowedOrigin,
          'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
          'Access-Control-Allow-Headers': 'Range, Origin, Accept, Content-Type',
          'Access-Control-Max-Age': '86400',
        }
      });
    }

    // Must be coming from the hamsterflix frontend, local dev, or the Pages preview domains
    if (!referer.includes('hamsterflix.neuralon.ai') && 
        !referer.includes('localhost') && 
        !referer.includes('127.0.0.1') && 
        !referer.includes('.hamsterflix.pages.dev')) {
      return new Response('Unauthorized Access: Hotlinking blocked. Access restricted to Hamsterflix.', { status: 403 });
    }

    // Extract file path from URL
    const objectKey = url.pathname.slice(1);
    
    if (!objectKey) {
      return new Response('Not Found', { status: 404 });
    }

    // Handle range requests to allow video streaming
    const rangeHeader = request.headers.get('Range');
    
    let object;
    if (rangeHeader) {
      object = await env.BUCKET.get(objectKey, {
        range: request.headers,
        onlyIf: request.headers
      });
    } else {
      object = await env.BUCKET.get(objectKey);
    }

    if (object === null) {
      return new Response('Object Not Found', { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('etag', object.httpEtag);
    headers.set('Access-Control-Allow-Origin', allowedOrigin);
    
    // EXTREME CACHING: Force browsers and the Cloudflare Edge network to cache media heavily for 30 days
    headers.set('Cache-Control', 'public, max-age=2592000, immutable');
    
    if (rangeHeader) {
      headers.set('Accept-Ranges', 'bytes');
      if (object.range) {
        headers.set('Content-Range', `bytes ${object.range.offset}-${object.range.offset + object.range.length - 1}/${object.size}`);
      }
      return new Response(object.body, { status: 206, headers });
    }

    return new Response(object.body, { headers });
  }
};
