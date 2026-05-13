// Highlight.js language definition for "filetree" (project tree)
// - connector/line characters (├ └ │ ─)
// - folder names ending with '/'
// - files with extensions
// - line comments starting with '#'

(function() {
  if (typeof hljs === 'undefined') return;
  if (hljs.getLanguage && hljs.getLanguage('filetree')) return;

  hljs.registerLanguage('filetree', function(hljs) {
    return {
      name: 'filetree',
      aliases: ['tree','file-tree'],
      case_insensitive: false,
      contains: [

        // comments beginning with #
        {
          className: 'comment',
          begin: /#.*$/,
          relevance: 0
        },

        // connector characters at start of line (├──, │, └──, etc.)
        {
          className: 'punctuation',
          begin: /^[\s│└├┬─]+/,
          relevance: 0
        },

        // folder names (ending with a slash)
        {
          className: 'section',
          begin: /[\w\-\.\/]+\//,
          relevance: 10
        },

        // file names (contain a dot)
        {
            className: 'property',
            begin: /[\w\-]*\.[\w\.]+/,
            relevance: 10
        },

        // fallback punctuation (any remaining box-drawing chars)
        {
          className: 'punctuation',
          begin: /[│└├┬─]+/,
          relevance: 0
        }
      ]
    };
  });
})();

