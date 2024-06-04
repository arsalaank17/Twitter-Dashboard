/*
 * This file is the demo for a block definition. For more information
 * see:
 * https://github.com/utwente-db/eca/wiki/Extending:-Creating-Your-Own-Blocks
 *
 */

(function($, block) {

    block.fn.image = function(config) {
        // handle configuration
        var options = $.extend({
            src:""
        }, config);
    
        // create HTML representation
        var $el = this.$element
        $el.attr("src",options.src)
        // create HTML element for display
        var data = {
            src: options.src
        }
    
        // update function to update element
        var update = function() {
            console.group(options.src)
            $el.attr("src", data.src)
        }
    
        // invoke update to initialise the display
        update();
    
        // register actions
        this.actions(function(e, message) {
                data.src = message.src;
                update();
        });
    
        // return the element for further work
        return this.$element;
    }
    
})(jQuery, block);
    