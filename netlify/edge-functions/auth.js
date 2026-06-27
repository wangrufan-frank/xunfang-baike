// "frank:150225" 的 Base64 = ZnJhbms6MTUwMjI1
const VALID_AUTH = 'Basic ZnJhbms6MTUwMjI1';

export default async (request, context) => {
  if (request.headers.get('authorization') === VALID_AUTH) {
    return context.next();
  }
  return new Response(null, {
    status: 401,
    headers: { 'WWW-Authenticate': 'Basic realm="xunfang-baike"' }
  });
};
