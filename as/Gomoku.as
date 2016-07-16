package  {
	
	import flash.events.*;
	import flash.display.*;
	import flash.text.*;
	//import flash.text.engine.*; 
	import flash.ui.*;
	//import fl.controls.*;
	import mx.controls.*;
	
	public class Gomoku extends MovieClip{
		const size:int = 500;
		const shift_x:int = 25;
		const shift_y:int = 35;
		const bg_color:uint = 0xb0b0b0;
		const gr_color:uint = 0x000000;
		
		public var game:Game;
		public var net:Net;
		
		public var desk:Sprite;
		public var selMode:ComboBox;
		public var newGame:Button;
		public var goStep:Button;
		public var goBack:Button;
		public var goRun:Button;
		public var statText:Label;
		public var c:Vector.<int>;
		//public var l = size - 2 * shift;
  		public var d:int = size / 16 + 1;
		public var steps:Vector.<Object>;
		public var texts:Vector.<TextField>;
		public var colors:Vector.<uint>;
		public var qsteps:int = 0;
		public var mode:int = 0;

		
		public function Gomoku() {
			// constructor code
			trace("Gomoku constructor started");
			
			desk = new Sprite();
			addChild(desk);
			
			selMode = new ComboBox();
			selMode.x = 16;
			selMode.y = 3;
			selMode.width = 70;
			newGame = new Button();
			goStep = new Button();
			goBack = new Button();
			goRun = new Button();
			statText = new Label();
			addChild(selMode);
			
			selMode.dataProvider.addItem({data: 0, label: "Manual"});
			selMode.dataProvider.addItem({data: 1, label: "Black"});
			selMode.dataProvider.addItem({data: 2, label: "Write"});
						
			desk.addEventListener(MouseEvent.MOUSE_MOVE, mouse_move);
			desk.addEventListener(MouseEvent.CLICK, mouse_click);
			selMode.addEventListener(Event.CHANGE, sel_mode);
			newGame.addEventListener(MouseEvent.CLICK, new_game);
			goStep.addEventListener(MouseEvent.CLICK, game_step);
			goRun.addEventListener(MouseEvent.CLICK, game_run);
			goBack.addEventListener(MouseEvent.CLICK, game_back);
			
			addEventListener(Event.ENTER_FRAME, draw);
			
			//statText.
			
			trace("Gomoku constructor finished");
		}
		
		public function draw(event:Event):void {
			trace("draw started");
			
			init();
			
			removeEventListener(Event.ENTER_FRAME, draw);
			addEventListener(Event.ENTER_FRAME, enterFrameHandler);
			
			trace("draw finished");
		}
		
		public function init():void {
			trace("init started");
			
			desk.x = shift_x;
			desk.y = shift_y;
			//desk.width = size;
			//desk.height = size;
			//trace(desk.x);
			
			goStep.enabled = false;
			goRun.enabled = false;
			goBack.enabled = false;
						
			game = new Game(this);
			net = new Net;
			c = new Vector.<int>(15);
			steps = new Vector.<Object>(225);
			texts = new Vector.<TextField>(225);
			for(var i: int = 0; i < 225; i++) {
				var s:String = (i + 1).toString();
				var txt:TextField = new TextField();
				txt.text = s;
				txt.width = d - (3 - s.length) * d/8;
				txt.height = d;
				txt.selectable = false;
				txt.visible = false;				
				texts[i] = txt;
			}
			colors = new Vector.<uint>(2);
			colors[0] = 0x000000;
			colors[1] = 0xffffff;
			trace("init finished");
		}
		
		public function status(txt: String): void {
			//statText.text = txt;
			statText.htmlText = "<P ALIGN='LEFT'><FONT FACE='Arial' SIZE='14' COLOR='#000000' LETTERSPACING='0' KERNING='0'>" + txt + "</FONT></P>"
		}
		
		protected function sel_mode(event:Event):void {
			//trace(selMode.selectedItem.label + selMode.selectedItem.data);
			mode = selMode.selectedItem.data;
		}
		
		protected function new_game(event:Event):void {
			desk_init();	
			game.play();
		}
		
		public  function desk_init() {
			for (var i:int = 0; i < desk.numChildren;)
				desk.removeChildAt(i);
			qsteps = 0;
			add_step(0, 0, "Start");
		}
		
		protected function game_step(event:Event):void {
			game.run(false);
		}
		
		protected function game_run(event:Event):void {
			game.run(true);
		}
		
		protected function game_back(event:Event):void {
			game.back();
		}
		
		protected function mouse_click(event:MouseEvent):void {
			if(game.is_play && !game.is_run && !game.is_busy) {
				var x:int = get_dc(event.localX);
				var y:int = get_dc(event.localY);
				if(x != -9 && y != -9 && net.get_point(x, y).s == 0) {
					//trace(x, y);
					game.go(false, x, y);
				}
			}
		}
		
		protected function mouse_move(event:MouseEvent):void {
			//trace(event);
			if(game.is_play && !game.is_run && !game.is_busy) {
				var x:int = get_dc(event.localX);
				var y:int = get_dc(event.localY);
				if(x != -9 && y != -9 && net.get_point(x, y).s == 0) {
					//trace(x, y);
					Mouse.cursor = MouseCursor.BUTTON;
				}
				else
					Mouse.cursor = MouseCursor.AUTO;
			}
		}
		
		protected function get_dc(v:int):int {
			for(var i:int = 0; i < 15; i++) {
				if(v < c[i] + d / 2 && v > c[i] - d / 2) 
        			return (i - 7);
			}
			return -9;
		}
			
		protected function enterFrameHandler(event:Event):void {
			desk.graphics.clear();
			draw_grid();
			draw_steps();
		}
				
		public function add_step(x:int, y:int, mes:String):void {
    		steps[qsteps] = {"x":x, "y":y, "mes":mes};
    		qsteps++;
  		}
		
		protected function draw_grid() {
			draw_border();
			
			c[7] = size/2;
			draw_vline(c[7]);
			draw_hline(c[7]);
			
			for(var i:int = 1; i < 8; i++) {
				c[7 - i] = c[7] - d * i;
      			c[7 + i] = c[7] + d * i;
      			draw_vline(c[7 + i]);
      			draw_vline(c[7 - i]);
      			draw_hline(c[7 + i]);
      			draw_hline(c[7 - i]);
			}
			
			function draw_border() {
				desk.graphics.lineStyle(2, gr_color);
				desk.graphics.beginFill(bg_color);
				desk.graphics.drawRect(0, 0, size, size);
				desk.graphics.endFill();
			}

			function draw_vline(x:int) {
				desk.graphics.lineStyle(1, gr_color);
				desk.graphics.moveTo(x, 0);
				desk.graphics.lineTo(x, size);
			}
		
			function draw_hline(y:int) {
				desk.graphics.lineStyle(1, gr_color);
				desk.graphics.moveTo(0, y);
				desk.graphics.lineTo(size, y);
			}
		}
		
		protected function draw_steps() {
			for(var i:int = 0; i < qsteps; i++)
				draw_step(steps[i], i);
				
			function draw_step(step:Object, n:int) {
				put(step.x, step.y, n, n%2);
			}
			
			function put(x:int, y:int, n:int, ic:int) {
				desk.graphics.lineStyle(1, gr_color);
				desk.graphics.beginFill(colors[ic]);
				desk.graphics.drawCircle(c[7 + x], c[7 + y], d / 2);
				desk.graphics.endFill();
								
				var txt:TextField = texts[n];
				txt.backgroundColor = colors[ic];
				txt.textColor = colors[1 - ic];
				txt.x = c[7 + x] - (d/3 + 2) + (3 - txt.length) * d/8;
				txt.y = c[7 + y] - d/3;
				txt.visible = true;
				if(!desk.contains(txt))
					desk.addChild(txt);
			}
			
		}
		
		
	}
	
}
