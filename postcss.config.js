module.exports = {
    plugins: [
        require('autoprefixer')({
            overrideBrowserslist: [
                'last 4 versions',
                'Safari >= 10',
                'iOS >= 10',
                'Firefox >= 52',
                'Edge >= 15'
            ]
        })
    ]
}
