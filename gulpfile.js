"use strict";
/* global require */

const del = require("del");
const gulp = require("gulp");
const run_sequence = require("run-sequence");

// Gulp plugins
const concat = require("gulp-concat");
const rename = require("gulp-rename");
const sourcemaps = require("gulp-sourcemaps");

// Set up Uglify plugin with ES6-compatible Uglify tool
const uglify_es = require("uglify-es");
const uglify_compose = require("gulp-uglify/composer");
const uglify = uglify_compose(uglify_es, console);

const BASE_DIR = "./js";
const BUILD_DIR = `${BASE_DIR}/build`;

const SRC_DIR = `${BASE_DIR}/src`;
const SRC_PATTERN = `${SRC_DIR}/**/*.js`;

const VENDOR_DIR = `${BASE_DIR}/vendor`;
const VENDOR_PATTERN = `${VENDOR_DIR}/**/*.js`;

const OUTPUT_DIR = "./static/js";

gulp.task("build:js", () => {
    return gulp.src([ // Set source directories
        `${SRC_DIR}/fouc.js`,  // Must be first to ensure libraries are loaded in time for the rest of the JS
        SRC_PATTERN,
        `${VENDOR_DIR}/moment/moment.js`, // Must be included before moment-timezone
        VENDOR_PATTERN], {base: "BASE_DIR"})
            .pipe(sourcemaps.init({largeFile: true})) // Initialise sourcemaps plugin
            .pipe(concat("all.js.tmp")) // Concatenate all JS files together
            .pipe(gulp.dest(BUILD_DIR)) // Write files to build dir
            .pipe(rename("script.js")) // Set new output filename
            .pipe(uglify({"mangle": false}).on("error", e => console.error(e))) // Minify the JS
            .pipe(sourcemaps.write()) // Write the sourcemaps
            .pipe(gulp.dest(OUTPUT_DIR)); // Write files to output dir
});

gulp.task("clean:js", () => {
    return del([ // Delete temporary files
        "js/build",
    ])
});

gulp.task("default", (cb) => {run_sequence("build:js", "clean:js", cb)});
