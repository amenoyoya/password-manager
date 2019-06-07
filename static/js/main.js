var app = new Vue({
    el: '#app',
    data: {
        categories: [],
        current_category: '',
        entries: [["a", "b", "c"]]
    },
    methods: {
        switch_category(category){
            app.current_category = category;
            this.display_passwords();
        },
        display_passwords(){
            axios.get('/data/passwords.json')
                .then(function(res) {
                    var entries = res.data[app.current_category];
                    if (entries) {
                        app.entries = entries;
                    }
                })
                .catch(function(err) {
                    console.log(err);
                })
        }
    }
});

axios.get('/data/categories.json')
    .then(function(res) {
        app.categories = res.data;
        if (app.categories.length > 0) {
            app.current_category = app.categories[0];
        }
    })
    .catch(function(err) {
        console.log(err);
    });

app.display_passwords();
