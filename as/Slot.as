package  {
	
	public class Slot {
		
		var net: Net;
		var scp: Point; 
		var d: int;
		var points: Array;
		var r: int = 0;
    	var s: int = 0;

		
		public function Slot(pnet: Net, pscp: Point, pd: int) {
			// constructor code
			net = pnet;
			scp = pscp;
			d = pd;
			points = new Array(5);
		}
		
		public function init() {
			points[2] = net.get_point(scp.x, scp.y);
			
			switch(d) {
				case 0:
					points[0] = net.get_point(scp.x, scp.y - 2);
            		points[1] = net.get_point(scp.x, scp.y - 1);
            		points[3] = net.get_point(scp.x, scp.y + 1);
            		points[4] = net.get_point(scp.x, scp.y + 2);
					break;
				case 1:
					points[0] = net.get_point(scp.x - 2, scp.y);
            		points[1] = net.get_point(scp.x - 1, scp.y);
            		points[3] = net.get_point(scp.x + 1, scp.y);
            		points[4] = net.get_point(scp.x + 2, scp.y);
					break;
				case 2:
					points[0] = net.get_point(scp.x - 2, scp.y - 2);
            		points[1] = net.get_point(scp.x - 1, scp.y - 1);
            		points[3] = net.get_point(scp.x + 1, scp.y + 1);
            		points[4] = net.get_point(scp.x + 2, scp.y + 2);
					break;
				case 3:
					points[0] = net.get_point(scp.x - 2, scp.y + 2);
            		points[1] = net.get_point(scp.x - 1, scp.y + 1);
            		points[3] = net.get_point(scp.x + 1, scp.y - 1);
            		points[4] = net.get_point(scp.x + 2, scp.y - 2);
					break;
			}
					
			for(var i:int = 0; i < 5; i++)
				points[i].add_slot(this);

		}

	}
	
}
