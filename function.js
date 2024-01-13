function handler(event) {
  var statusCode =
    (event.request.querystring.code && event.request.querystring.code.value) ||
    400;
  return {
    statusCode: Number(statusCode),
  };
}
