
        $('#id_{self.elem_id} ')
        $( "#slider-range-{self.elem_id}" ).slider({{
        range: true,
        min:  {self.minimum},
        max:  {self.maximum},
        step:  {self.step} ,
        values: [  {self.initialMin} , {self.initialMax}  ],
        slide: function( event, ui ) {{  
          $( "#id_ {self.elem_id} " ).val("  {self.elem_name}  "+ ui.values[ 0 ] + " - " + ui.values[ 1 ] );   
          document.getElementById("match_form").submit();
        }},
        change: function() {{
          document.getElementById("match_form").submit();
        }}
        }});
        $( "#id_{self.elem_id} " ).val(" {self.elem_name} "+ $( "#slider-range-{self.elem_id}" ).slider( "values", 0 ) +
        " - " + $( "#slider-range-{self.elem_id}" ).slider( "values", 1 ) );  
