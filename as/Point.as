package  {
	
	public class Point {
		
		var net: Net;
		var x:int;
		var y:int;
		var slots:Array; // = ArrayBuffer.empty[Slot]
    	var r:Array; // = Array[Byte](0, 0, 0)
    	var s:int = 0;

		public function Point(pnet: Net, px:int, py:int) {
			// constructor code
			net = pnet;
			x = px;
			y = py;
			slots = new Array();
			r = [0, 0, 0];
		}
		
    	public function add_slot(s: Slot) {
      		slots.push(s);
      		r[s.s]++;
    	}
		
    	public function is_valid_scp(d: int): Boolean {
			//// 0 - vert, 1 - horiz, 2 - up, 3 - down
      		if (d == 0 && y > -6 && y < 6) 
				return true;
      		if (d == 1 && x > -6 && x < 6)
				return true;
      		if (d == 2 && (x > -6 && y < 6) && (x < 6 && y > -6))
				return true;
      		if (d == 3 && (x > -6 && y > -6) && (x < 6 && y < 6))
				return true;
      		return false;
    	}
  	}
}
