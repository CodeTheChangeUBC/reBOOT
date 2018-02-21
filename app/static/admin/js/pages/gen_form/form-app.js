requirejs.config({
    baseUrl: '../static/admin/js/pages/gen_form',
    paths: {
        app: '../gen_form'
    }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['app/form-main']);