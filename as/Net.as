package  {
	
	public class Net {
		const N: int = 225;
  		const F: int = 5;
	
  		var all_points:Vector.<Point>; //= Array.ofDim[Point](15, 15)
  		var all_slots:Vector.<Slot>; //= ArrayBuffer.empty[Slot]
	
  		var empty_points:Vector.<Point>; //= ArrayBuffer.empty[Point]
  		var active_slots:Vector.<Vector.<Slot>>; //= Array.ofDim[ArrayBuffer[Slot]](3)

		public function Net() {
			// constructor code
			active_slots = new Vector.<Vector.<Slot>>(3);
			all_points = new Vector.<Point>(225);
		}
		
		public function init():void {
			active_slots[0] = new Vector.<Slot>(); // free
			active_slots[1] = new Vector.<Slot>(); // black
			active_slots[2] = new Vector.<Slot>(); // white
			
			empty_points = new Vector.<Point>();
			all_slots = new Vector.<Slot>();
			
			for(var i:int = 0; i < 225; i++) {
				var p:Point = new Point(this, Math.floor(i / 15) - 7, i % 15 - 7);
				//trace(i, p.x, p.y);
				all_points[i] = p;
				empty_points.push(p);
				
				for (var j:int = 0; j < 4; j++) {
					if(p.is_valid_scp(j)) {
						var s: Slot = new Slot(this, p, j);
						all_slots.push(s);
						active_slots[0].push(s);
					}
				}
			}
			
			for each(var item: Slot in all_slots) {
				item.init();
			}
		}
		
		public function step(x:int, y:int, c:int) {
    		var p:Point = get_point(x, y);
    		p.s = c;
			empty_points.splice(empty_points.indexOf(p), 1);
		
    		for each(var s:Slot in p.slots) {
      			if(s.s == 0) {
        			p.r[0]--;
        			p.r[c]++;
        			s.s = c;
        			s.r = 1;
        			active_slots[0].splice(active_slots[0].indexOf(s),1);
        			active_slots[c].push(s);
      			}
      			else if(s.s == c) {
        			p.r[c]++;
        			s.r++;
      			}
      			else if(s.s != 3) {
        			p.r[c]--;
					active_slots[s.s].splice(active_slots[s.s].indexOf(s),1);
        			s.s = 3;
      			}	
			}
		}
		
		public function get_point(x: int, y: int): Point {
			//trace(x, y, (x + 7) * 15 + (y + 7));
			var p:Point = all_points[(x + 7) * 15 + (y + 7)];
			//trace(p);
			return p;
		}


	}
	
}
