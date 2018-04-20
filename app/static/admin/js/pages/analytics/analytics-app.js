requirejs.config({
  baseUrl: "../static/admin/js/pages/analytics",
  paths: {
    app: "."
  }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(["app/analytics-main"]);
