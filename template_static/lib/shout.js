/*
 * This file is the demo for a block definition. For more information
 * see:
 * https://github.com/utwente-db/eca/wiki/Extending:-Creating-Your-Own-Blocks
 *
 */

(function($, block) {

block.fn.shout = function(config) {
    // handle configuration
    var options = $.extend({
        size: '12pt',
        text: '0',
        color: 'white'
    }, config);

    // create HTML representation
    var $el = $('<span style="color=white"></span>').appendTo(this.$element);
    $el.css('font-size', options.size);

    // create HTML element for display
    var data = {
        text: options.text,
        color: options.color
    }

    // update function to update element
    var update = function() {
        $el.text(data.text).css('color', data.color);
    }

    // invoke update to initialise the display
    update();

    // register actions
    this.actions(function(e, message) {
            data.text = message.text;
            update();
    });

    // return the element for further work
    return this.$element;
}

})(jQuery, block);
