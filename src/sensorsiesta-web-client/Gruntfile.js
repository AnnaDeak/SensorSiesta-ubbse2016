/**
 * Souce files
 */

external_js = ["./node_modules/jquery/dist/jquery.min.js",
               "./node_modules/tether/dist/js/tether.min.js",
               "./node_modules/bootstrap/dist/js/bootstrap.min.js",
               "./node_modules/knockout/build/output/knockout-latest.js",
               "./node_modules/canvasjs/dist/jquery.canvasjs.min.js"];

external_css = ["./node_modules/tether/dist/css/tether.min.css",
                "./node_modules/bootstrap/dist/css/bootstrap.min.css"];
                

dist = "../sensorsiesta-server/static";


// configure Grunt

module.exports = function(grunt) {

	grunt.initConfig({
		
		// clean dist folder
		clean: {
			js:    [ dist + '/**/*.js' ],
			css:   [ dist + '/**/*.css' ],
			html:  [ dist + '/*.html' ],
			options: {
				force: true
			}
		},
		
		// minify internal files
		uglify: {
			js: {
				files: [
				    { expand: true, cwd: 'js', src: './**/*.js', dest: dist }
				]
			}
		},
		
		cssmin: {
			css: {
				files: [
				    { expand: true, cwd: 'css', src: './**/*.css', dest: dist }
				]
			}
		},
		
		htmlmin: {
			html: {
				options: {
					removeComments: true,
					collapseWhitespace: true
				},
				files: [
				    { expand: true, src: './*.html', dest: dist }
				]
			}
	    },
	    
	    // copy internal files (for debug mode)
	    copy: {
	    	js: {
				files: [
				    { expand: true, cwd: 'js', src: './**/*.js', dest: dist },
				]
			},
		    css: {
		    	files: [
	    	        { expand: true, cwd: 'css', src: './**/*.css', dest: dist },
    	        ]
		    },
		    html: {
		    	files: [
	    	        { expand: true, src: './*.html', dest: dist }
    	        ]
		    }
	    },
	    
		// concatenate all JS/CSS files into one 
		concat: {
			js: {
				src: [external_js],
				dest: dist + '/external.min.js'
			},
			css: {
				src: [external_css],
				dest: dist + '/external.min.css'
			}
		},
		
		// configure JShint
		jshint: {
			files: ['./js/**/*.js'],
			options: {
				force: true
			}
		},
	
		// watch for changes of internal files
		watch: {
			js: {
				files: ['./js/**/*.js'],
				tasks: ['clean:js', 'uglify:js', 'concat:js']
			},
			jsdebug: {
				files: ['./js/**/*.js'],
				tasks: ['jshint', 'clean:js', 'copy:js', 'concat:js']
			},
			css: {
				files: ['./css/**/*.css'],
				tasks: ['clean:css', 'cssmin:css', 'concat:css']
			},
			cssdebug: {
				files: ['./css/**/*.css'],
				tasks: ['clean:css', 'copy:css', 'concat:css']
			},
			html: {
				files: ['./*.html'],
				tasks: ['clean:html', 'htmlmin:html']
			},
			htmldebug: {
				files: ['./*.html'],
				tasks: ['clean:html', 'copy:html']
			}
		},
		
		concurrent: {
			options: {
			    logConcurrentOutput: true
			},
		    watchProd: ['watch:js', 'watch:css', 'watch:html'],
		    watchDebug: ['watch:jsdebug', 'watch:cssdebug', 'watch:htmldebug']
		}
	});
	
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-htmlmin');
	grunt.loadNpmTasks('grunt-contrib-copy');
	grunt.loadNpmTasks('grunt-concurrent');
	
	// start tasks by default
	grunt.registerTask('deploy',      ['clean', 'concat', 'uglify', 'cssmin', 'htmlmin']);
	grunt.registerTask('deployDebug', ['clean', 'concat', 'copy', 'jshint']);
	grunt.registerTask('default',     ['deploy',      'concurrent:watchProd']);
	grunt.registerTask('debug',       ['deployDebug', 'concurrent:watchDebug']);

};
