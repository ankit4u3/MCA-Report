Rules Layout.XML

<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
android:background="#ffffff"
    android:orientation="vertical" >

    <TextView
        android:id="@+id/tvrules"
        android:layout_width="match_parent"
        android:layout_height="60dp"
        android:layout_gravity="center_horizontal"
        android:background="@drawable/roughlabel"
        android:gravity="center"
        android:padding="5dp"
        android:shadowColor="#FEE"
        android:shadowDx="0"
        android:shadowDy="0"
        android:shadowRadius="3"
        android:text="How to play"
        android:textColor="#FFF"
        android:textSize="25dp" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="0.90"
        android:orientation="vertical" >

        <ViewFlipper
            android:id="@+id/flipper"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content" >

            <ImageView
                android:id="@+id/imageView1"
                android:layout_width="fill_parent"
                android:layout_height="fill_parent"
                android:src="@drawable/htp1" />
        </ViewFlipper>
    </LinearLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="0.04"
        android:gravity="right"
        android:orientation="horizontal" >

        <Button
            android:id="@+id/buttonHowNext"
            android:layout_width="140dp"
            android:layout_height="55dp"
            android:layout_gravity="right"
            android:background="@drawable/roughbtn"
            android:drawableRight="@drawable/arright"
            android:text="Next"
            android:textColor="#Fee" />
    </LinearLayout>

</LinearLayout>

Rules.java Source Code

package in.electromedica.in.treasurehunt;
public class RulesActivity extends Activity {
	static Button nextbtn;
	static public int viewnum = 0;
	ImageView imgview;
	int list[] = { R.drawable.htp1, R.drawable.htp2, R.drawable.htp3,
			R.drawable.htp4 };
	private static final int SWIPE_MIN_DISTANCE = 120;
	private static final int SWIPE_MAX_OFF_PATH = 250;
	private static final int SWIPE_THRESHOLD_VELOCITY = 200;
	private GestureDetector gestureDetector;
	View.OnTouchListener gestureListener;
	private Animation slideLeftIn;
	private Animation slideLeftOut;
	private Animation slideRightIn;
	private Animation slideRightOut;
	private ViewFlipper viewFlipper;
	public static WindowManager.LayoutParams lp;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// overridePendingTransition(R.anim.slide_in_right,
		// R.anim.slide_out_left);
		setContentView(R.layout.rules_layout);
		lp = getWindow().getAttributes();
		checkBrightness();
		nextbtn = (Button) findViewById(R.id.buttonHowNext);
		imgview = (ImageView) findViewById(R.id.imageView1);
		if (viewnum == 3) {
			nextbtn.setText("Play game");
		}
		new Thread(new Runnable() {

			public void run() {
				// TODO Auto-generated method stub
				imgview.setImageResource(list[viewnum]);
			}
		}).run();

		viewFlipper = (ViewFlipper) findViewById(R.id.flipper);
		slideLeftIn = AnimationUtils.loadAnimation(this, R.anim.slide_in_left);
		slideLeftOut = AnimationUtils
				.loadAnimation(this, R.anim.slide_out_left);
		slideRightIn = AnimationUtils
				.loadAnimation(this, R.anim.slide_in_right);
		slideRightOut = AnimationUtils.loadAnimation(this,
				R.anim.slide_out_right);

		gestureDetector = new GestureDetector(new MyGestureDetector());
		gestureListener = new View.OnTouchListener() {
			public boolean onTouch(View v, MotionEvent event) {
				if (gestureDetector.onTouchEvent(event)) {
					return true;
				}
				return false;
			}
		};

		nextbtn.setOnClickListener(new View.OnClickListener() {

			public void onClick(View v) {
				nextrule();
			}
		});

	}

	@Override
	public void onBackPressed() {
		// TODO Auto-generated method stub
		viewnum = 0;
		finish();
		overridePendingTransition(R.anim.slide_in_top, R.anim.slide_out_bottom);
	}

	public void nextrule() {
		Intent i;
		if (viewnum == 3) {
			viewnum = 0;
			i = new Intent(RulesActivity.this, MainActivity.class);
			imgview.destroyDrawingCache();
			finish();
			startActivity(i);
		} else {
			i = new Intent(RulesActivity.this, RulesActivity.class);
			viewnum = viewnum + 1;
			imgview.destroyDrawingCache();
			startActivity(i);
			overridePendingTransition(R.anim.slide_in_right,
					R.anim.slide_out_left);
			finish();
		}
	}

	public void prevrule() {
		Intent i;
		if (viewnum == 0) {
			return;
		} else {
			i = new Intent(RulesActivity.this, RulesActivity.class);
			viewnum = viewnum - 1;
			imgview.destroyDrawingCache();
			startActivity(i);
			overridePendingTransition(R.anim.slide_in_left,
					R.anim.slide_out_right);
			finish();
		}
	}

	class MyGestureDetector extends SimpleOnGestureListener {
		@Override
		public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,
				float velocityY) {
			try {
				if (Math.abs(e1.getY() - e2.getY()) > SWIPE_MAX_OFF_PATH)
					return false;
				// right to left swipe
				if (e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE
						&& Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
					nextrule();
					}
			} catch (Exception e) {
				// nothing
			}
			return false;
		}
	}

	@Override
	public boolean onTouchEvent(MotionEvent event) {
		if (gestureDetector.onTouchEvent(event))
			return true;
		else
			return false;
	}

	public void checkBrightness() {
		if (!MainActivity.isBright) {
			lp.screenBrightness = MainActivity.initBright;
			getWindow().setAttributes(lp);
			MainActivity.isBright = false;
		} else {
			lp.screenBrightness = (float) 1;
			getWindow().setAttributes(lp);
			MainActivity.isBright = true;
		}

	}

	@Override
	protected void onResume() {
		checkBrightness();
		super.onResume();
	}

}
