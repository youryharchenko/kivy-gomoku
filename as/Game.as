package  {
	
	//import _AS3_.vec.Vector;
	
	public class Game {
		
		public var app:Gomoku;
		public var is_play:Boolean = false;
		public var is_run:Boolean = false;
		public var is_busy:Boolean = false;
		
		public var n_step: int = 0;
  		public var mes: String = "";

		
		public function Game(a:Gomoku) {
			// constructor code
			app = a;
			app.status("Press 'New'");
		}
		
		public function play():void {
			is_busy = false;
		    is_play = true;
    		is_run = false;

			app.selMode.enabled = false;
			
			if(app.mode == 0)
				app.goStep.enabled = true;
			else {
				app.goStep.enabled = false;
				app.goBack.enabled = false;
			}
				
			app.goRun.enabled = true;
			
			app.net.init();
			
			mes = "Start";
    		n_step = 1;
    		app.net.step(0, 0, 1);
			app.status("New game");
			
			if(app.mode == 1) {
				run(false);
			}
		}
		
		public function run(r: Boolean):void {
			if(is_play) {
      			app.status("Thinking...");
      			is_busy = true;
      			is_run = r;
      			go(true, 0, 0);
      			is_busy = false;
    		}
		}
		
		public function back():void {
    		is_play = true;
    		is_busy = true;
			
    		replay(1);
			
    		is_busy = false;
        
    		app.goRun.enabled = true;
    		app.goStep.enabled = true;
  		}

		
		public function go(auto: Boolean, x: int, y: int): void {
			var ret:int; 
			if(auto) 
				ret = next_step();
			else 
				ret = manual_step(x, y);

    		app.status(ret < 0 ? "Finish! -> " +  mes : "Step " + ret + " -> " + mes);
		
    		if(app.mode == 0)
				app.goBack.enabled = true;

    		if(ret < 0 || ret > 224) {
		    	app.goRun.enabled = false;
      			app.goStep.enabled = false;
				app.selMode.enabled = true;
	
      			is_run = false;
      			is_play = false;
    		}
			else if(!auto && app.mode > 0) go(true, 0, 0);
    		else if(is_run) go(true, 0, 0)
  		}
		
		public function replay(k: int): void {
    		var n:int = n_step - k;
		
    		if(n > 0) {
      			app.net.init();
				app.desk_init();
      			n_step = 1;
    			app.net.step(0, 0, 1);
      
			    is_busy = false;
      			is_play = true;
      			is_run = false;
			
      			app.status("Start");
    		}
		
    		if(n > 1) {
				var st: Object = null;
			
      			for(var i:int = 1; i < n; i++) {
        			st = app.steps[i];
        			app.steps[i] = null;
        			replay_step(st.x, st.y, st.mes);
      			}

      			app.status("Step " + n_step + " -> " + st.mes);
    		}
  		}
		
		public function next_step(): int {
    		n_step++;
		
    		if(check_win(3 - (2 - n_step%2)) || check_draw()) 
				return -1;
    		else {
      			var p: Point = calc_point(2 - n_step%2);
      			app.net.step(p.x, p.y, 2 - n_step%2);
      			app.add_step(p.x, p.y, mes);
      			return n_step;
    		}
  		}
		
		public function manual_step(x: int, y: int): int {
    		n_step++;
		
		    if(check_win(3 - (2 - n_step%2)) || check_draw()) 
				return -1;
    		else {
      			app.net.step(x, y, 2 - n_step%2);
      			mes = name_c(2 - n_step%2) + " :: manual (" + x + ":" + y + ")";
      			app.add_step(x, y, mes);
      			return n_step;
    		}
  		}
		
		protected function replay_step(x: int, y: int, mes: String): int {
    		n_step++;
    		app.net.step(x, y, 2 - n_step%2);
    		app.add_step(x, y, mes);
    		return n_step;
  		}
		
		protected function check_win(c: int): Boolean {
    		for each(var s:Slot in app.net.active_slots[c]) {
      			if (s.r == 5) {
        			mes = name_c(c) + " :: win!!!";
        			return true;
      			}
			}
    		return false;
  		}
		
		protected function check_draw(): Boolean {
    		if(app.net.active_slots[0].length == 0 &&
       			app.net.active_slots[1].length == 0 &&
       			app.net.active_slots[2].length == 0) {
      				mes = " draw :(";
      				return true;
    		}
    		else 
				return false;
		}
		
		protected function calc_point(c:int):Point {
			var ret: Vector.<Object>;
		    mes = name_c(c) + " :: auto :: ";
			
			ret = find_slot_4(c);
    		if(ret.length == 0) ret = find_slot_4(3 - c);
		
    		if(ret.length == 0) ret = find_point_x(c, 2, 1);
    		if(ret.length == 0) ret = find_point_x(3 - c, 2, 1);
        
    		if(ret.length == 0) ret = find_point_x(c, 1, 5);
    		if(ret.length == 0) ret = find_point_x(3 - c, 1, 5);
        
    		if(ret.length == 0) ret = find_point_x(c, 1, 4);
    		if(ret.length == 0) ret = find_point_x(3 - c, 1, 4);
        
    		if(ret.length == 0) ret = find_point_x(c, 1, 3);
    		if(ret.length == 0) ret = find_point_x(3 - c, 1, 3);
        
    		if(ret.length == 0) ret = find_point_x(c, 1, 2);
    		if(ret.length == 0) ret = find_point_x(3 - c, 1, 2);
        
    		if(ret.length == 0) ret = find_point_x(c, 1, 1);
    		if(ret.length == 0) ret = find_point_x(3 - c, 1, 1);
        
    		if(ret.length == 0) ret = find_point_x(c, 0, 10);
    		if(ret.length == 0) ret = find_point_x(3 - c, 0, 10);
		
    		if(ret.length == 0) ret = find_point_x(c, 0, 9);
    		if(ret.length == 0) ret = find_point_x(3 - c, 0, 9);
        
    		if(ret.length == 0) ret = find_point_x(c, 0, 8);
    		if(ret.length == 0) ret = find_point_x(3 - c, 0, 8);
        
    		if(ret.length == 0) ret = find_point_x(c, 0, 7);
    		if(ret.length == 0) ret = find_point_x(3 - c, 0, 7);
                    
    		if(ret.length == 0) ret = calc_point_max_rate(c);
			
			//mes = ret[0].m;
			//return ret[0].p;
			var i:int = Math.floor(Math.random() * ret.length);
			mes = ret[i].m;
			return ret[i].p;
		}
		
		protected function find_slot_4(c:int):Vector.<Object> {
			var ret: Vector.<Object> = new Vector.<Object>();
			var m: String;
			for each(var s:Slot in app.net.active_slots[c]) {
      			if (s.r == 4) {
        			for each(var p:Point in s.points) {
          				if(p.s == 0) {
            				m = mes + name_c(c) + " :: find_slot_4 -> (" + p.x + ":" + p.y + ")";
            				ret.push({"p": p, "m": m});
		  				}
					}
				}
			}
        	return ret;
		}
		
		protected function find_point_x(c: int, r: int, b: int): Vector.<Object> {
			var ret: Vector.<Object> = new Vector.<Object>();
			var m: String;
            for each(var p: Point in app.net.empty_points) {
        		var i:int = 0;
        		for each(var s: Slot in p.slots) {
          			if(s.s == c && s.r > r) i++;
				}
        		if(i > b) {
          			m = mes + name_c(c) + " :: find_point_x(" + r + ", " + b + ") -> (" + p.x + ":" + p.y + ")";
          			ret.push({"p": p, "m": m});
        		}
      		}
        	return ret;
		}

		protected function calc_point_max_rate(c: int): Vector.<Object> {
    		var ret: Vector.<Object>;
			var m: String;
            var r:int = -1;
    		var d:int = 0;
			var i:int = 0;
			
    		for each(var p: Point in app.net.empty_points) {
        		d = 0;
        		for each(var s: Slot in p.slots) {
          			if(s.s == 0) d++;
          			else if(s.s == c) d += (1 + s.r) * (1 + s.r); //+ 0.5f
          			else if(s.s != 3) d += (1 + s.r) * (1 + s.r);
				}
        		if(d > r) {
					i = 1;
          			r = d;
					ret = new Vector.<Object>();
					m = mes + name_c(c) + " :: point_max_rate(" + i + ", " + r + ") -> (" + p.x + ":" + p.y + ")";
					ret.push({"p": p, "m": m});
        		}
				else if(d == r) {
					i++;
					m = mes + name_c(c) + " :: point_max_rate(" + i + ", " + r + ") -> (" + p.x + ":" + p.y + ")";
					ret.push({"p": p, "m": m});
				}
      		}
    		return ret;
  		}

		
		protected function name_c(c: int): String {
    		return (c == 1) ? "black" : "white";
		}

	}
}
