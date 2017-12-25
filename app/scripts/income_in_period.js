$(function () {
    var accounts = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        //prefetch: '../data/films/post_1960.json',
        remote: {
          url: '/account/search/%QUERY',
          wildcard: '%QUERY'
        }
      });
      
      $('#accounts.typeahead').typeahead(null, {
        name: 'best-pictures',
        display: 'value',
        source: accounts
      });    
});
