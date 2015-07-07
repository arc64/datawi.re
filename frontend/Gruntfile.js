module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-html2js');

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    connect: {
      server: {
        port: 3000,
        base: '.'
      }
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        files: [
            {
                src: ['dist/<%= pkg.name %>.js', 'dist/templates.js'],
                dest: 'dist/<%= pkg.name %>.min.js'
            },
            {
                src: ['bower_components/angular/angular.js',
                      'bower_components/ng-debounce/angular-debounce.js',
                      'bower_components/angular-route/angular-route.js',
                      'bower_components/angular-animate/angular-animate.js',
                      'bower_components/angular-loading-bar/build/loading-bar.js',
                      'bower_components/angular-truncate/src/truncate.js',
                      'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
                      'bower_components/nginfinitescroll/build/ng-infinite-scroll.js'],
                dest: 'dist/vendor.js'
            }
        ]
      }
    },
    concat: {
      options: {
        stripBanners: true,
        separator: ';'
      },
      dist: {
        src: ['js/app.js', 'js/**/*.js'],
        dest: 'dist/<%= pkg.name %>.js'
      },
    },
    html2js: {
      dist: {
        options: {
          base: '.',
          module: 'datawire.templates'
        },
        src: ['templates/**/*.html'],
        dest: 'dist/templates.js'
      }
    },
    less: {
      development: {
        options: {
          paths: ["less"],
          strictImports: true
        },
        files: {
          "dist/app.css": ["style/style.less"]
        }
      }
    },
    watch: {
      templates: {
        files: ['templates/**/*.html'],
        tasks: ['html2js']
      },
      js: {
        files: ['src/**/*.js'],
        tasks: ['concat', 'uglify']
      },
      style: {
        files: ['less/**/*.less'],
        tasks: ['less']
      },
    }
  });

  grunt.registerTask('default', ['less', 'html2js', 'concat', 'uglify']);
  grunt.registerTask('server', ['connect', 'watch'])
};
