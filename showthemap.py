Show the Map XML

<?xml version="1.0" encoding="utf-8"?>
<FrameLayout
  xmlns:android="http://schemas.android.com/apk/res/android"
  android:layout_width="fill_parent"
  android:layout_height="fill_parent">
  
  
  <view android:id="@+id/mv"
    class="com.google.android.maps.MapView"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:layout_weight="1" 
    android:clickable="true"
    android:apiKey="0yccAvyjhO4iYUJ3hXXXXXX-FGe3NkO9YXXXXXX"
    />
    
    <!-- Must replace apiKey above with appropriate version below -->
   	<!-- for M33:  android:apiKey="07WVUg-srWUbhpkGj1mi0w56xD9nMEu0NhqJeYg" -->
   	<!-- for M81:  android:apiKey="07WVUg-srWUY6iEC2qTEiuT1mKYkoo6EVPK74pA" --> 
   	<!-- for Castor: android:apiKey="07WVUg-srWUbTcCW-uHqNQR4SdYngQOCgmJN60A" -->
   	
  <LinearLayout
    android:orientation="horizontal"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content" 
    android:padding="0px"           
    >
                                            
  <Button
      android:id="@+id/doOverlay"
      android:layout_width="fill_parent"
      android:layout_height="wrap_content"
      android:layout_marginLeft="30px"
      android:layout_weight="1.0"
      android:text="Hunt Locations"
      android:textSize="12sp" />
    
  <Button
      android:id="@+id/doAccess"
      android:layout_width="fill_parent"
      android:layout_height="wrap_content"
      android:layout_weight="1.0"
      android:text="Team Position"
      android:textSize="12sp" />
    
  <Button android:id="@+id/doRoute"
    android:layout_width="fill_parent"
    android:layout_height="wrap_content"
    android:layout_marginRight="30px"
    android:layout_weight="1.0"
    android:textSize="12sp" 
    android:text="Route" />
                
  </LinearLayout>
   		
</FrameLayout>

Showthemap.java
package in.electromedica.in.treasurehunt;
public class ShowTheMap extends MapActivity {

	private static double lat;
	private static double lon;
	private int latE6;
	private int lonE6;
	private MapController mapControl;
	private GeoPoint gp;
	private MapView mapView;

	private Button overlayButton, accessButton;
	private Button routeButton;
	private List<Overlay> mapOverlays;
	private Drawable drawable1, drawable2;
	private MyItemizedOverlay itemizedOverlay1, itemizedOverlay2;
	private boolean foodIsDisplayed = false;
	private ArrayList<Address> multipleMapAddresses;// = ArrayList<Address>();
	// Define an array containing the food overlay items
	QuestionDataSource datasource;
	Question q;
	int pos;
	String nick;
	String response;
	LocationManager locationManager;
	Location pointLocation;
	LocationListener listen;
	MotionEvent e;

	private final OverlayItem[] foodItem = {
			new OverlayItem(new GeoPoint(35952967, -83929158), "Food Title 1",
					"Food snippet 1"),
			new OverlayItem(new GeoPoint(35953000, -83928000), "Food Title 2",
					"Food snippet 2"),
			new OverlayItem(new GeoPoint(35955000, -83929158), "Food Title 3",
					"Food snippet 3") };

	// Define an array containing the access overlay items

	private OverlayItem[] accessItem;// = {


	String TAG = "GPStest";
	// Set up the array of GeoPoints defining the route
	int numberRoutePoints;
	GeoPoint routePoints[]; // Dimension will be set in class RouteLoader below
	int routeGrade[]; // Index for slope of route from point i to point i+1
	RouteSegmentOverlay route; // This will hold the route segments
	boolean routeIsDisplayed = false;
	private ArrayList<Long> values;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// requestWindowFeature(Window.FEATURE_NO_TITLE); // Suppress title bar
		// for
		// more space
		setContentView(R.layout.showthemap);

		multipleMapAddresses = new ArrayList<Address>();
		datasource = new QuestionDataSource(this);
		datasource.open();
		values = datasource.getAllIds();

		// Add map controller with zoom controls
		mapView = (MapView) findViewById(R.id.mv);
		mapView.setSatellite(false);
		mapView.setTraffic(false);
		mapView.setBuiltInZoomControls(true); // Set android:clickable=true in
												// main.xml

		int maxZoom = mapView.getMaxZoomLevel();
		int initZoom = maxZoom - 2;
		mapControl = mapView.getController();
		mapControl.setZoom(initZoom);
		// Convert lat/long in degrees into integers in microdegrees
		latE6 = (int) (lat * 1e6);
		lonE6 = (int) (lon * 1e6);
		gp = new GeoPoint(latE6, lonE6);
		mapControl.animateTo(gp);
		mapOverlays = mapView.getOverlays();
		drawable1 = this.getResources().getDrawable(R.drawable.chest);
		itemizedOverlay1 = new MyItemizedOverlay(drawable1,
				getApplicationContext());
		itemizedOverlay1.addOverlay(new OverlayItem(gp, "You'r Possition is ",
				"Click & Save"));
		mapOverlays.add(itemizedOverlay1);

		for (int ptr = 0; ptr < values.size(); ptr++) {
			Question q = datasource.getQsAtId(ptr);
			Log.d("map", q.getQuestion());//

			Double l;
			Double n;
			int lc, nc;
			l = Double.valueOf(q.getLatitude());
			n = Double.valueOf(q.getLongitute());
			lc = (int) (l * 1e6);
			nc = (int) (n * 1e6);

			itemizedOverlay1.addOverlay(new OverlayItem(new GeoPoint(lc, nc), q
					.getQuestion(), "THis is Sparta"));
			mapControl.animateTo(new GeoPoint(lc, nc));

		}

		mapView.postInvalidate();
		// Button to control food overlay
		overlayButton = (Button) findViewById(R.id.doOverlay);
		overlayButton.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				// setOverlay1();
			}
		});

		// Button to control access overlay
		accessButton = (Button) findViewById(R.id.doAccess);
		accessButton.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				// setOverlay2();
				AlertDialog.Builder alert = new AlertDialog.Builder(
						getApplicationContext());
				alert.setTitle("Alert DIalog With EditText"); // Set Alert
																// dialog title
																// here
				alert.setMessage("Enter your Name Here"); // Message here

				alert.setPositiveButton("OK",
						new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog,
									int whichButton) {
								// String value = input.getText().toString();
								// Do something with value!
								// You will get input data in this variable.
								dialog.dismiss();

							}
						});

				alert.setNegativeButton("CANCEL",
						new DialogInterface.OnClickListener() {
							public void onClick(DialogInterface dialog,
									int whichButton) {
								// Canceled.
								dialog.cancel();
							}
						});
				AlertDialog alertDialog = alert.create();
				alertDialog.show();
				/* Alert Dialog Code End */
			}

		});

		// Button to control route overlay
		routeButton = (Button) findViewById(R.id.doRoute);
		routeButton.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {
				if (!routeIsDisplayed) {
					routeIsDisplayed = true;
					loadRouteData();
				} else {
					if (route != null)
						route.setRouteView(false);
					route = null; // To prevent multiple route instances if key
									// toggled rapidly (see line 235)
					routeIsDisplayed = false;
					mapView.postInvalidate();
				}
			}
		});

	}

	/*
	 * Methods to set map overlays. In this case we will place a small overlay
	 * image at a specified location. Place the marker image as a png file in
	 * res > drawable-* . For example, the reference to
	 * R.drawable.knifefork_small below is to an image file called
	 * knifefork_small.png in the project folder res > drawable-hdpi. Can only
	 * use lower case letters a-z, numbers 0-9, ., and _ in these image file
	 * names. In this example the single overlay item is specified by drawable
	 * and the location of the overlay item is specified by overlayitem.
	 */

	// Display food location overlay. If not already displayed, clicking button
	// displays all
	// food overlays. If already displayed successive clicks remove items one by
	// one. This
	// illustrates ability to change individual overlay items dynamically at
	// runtime.

	public void setOverlay1() {
		int foodLength = foodItem.length;
		// Create itemizedOverlay2 if it doesn't exist and display all three
		// items
		if (!foodIsDisplayed) {
			mapOverlays = mapView.getOverlays();
			drawable1 = this.getResources().getDrawable(
					R.drawable.knifefork_small);
			itemizedOverlay1 = new MyItemizedOverlay(drawable1,
					getApplicationContext());
			// Display all three items at once

			for (int i = 0; i < foodLength; i++) {

				itemizedOverlay1.addOverlay(foodItem[i]);
				// itemizedOverlay1.addOverlay(overlay)
			}
			mapOverlays.add(itemizedOverlay1);
			foodIsDisplayed = !foodIsDisplayed;

			// Remove each item successively with button clicks
		} else {
			itemizedOverlay1.removeItem(itemizedOverlay1.size() - 1);
			if ((itemizedOverlay1.size() < 1))
				foodIsDisplayed = false;
		}
		// Added symbols will be displayed when map is redrawn so force redraw
		// now
		mapView.postInvalidate();
	}

	// Display accessibility overlay. If not already displayed, successive
	// button clicks display each of
	// the three icons successively, then the next removes them all. This
	// illustrates the ability to
	// change individual overlay items dynamically at runtime.

	public void setOverlay2() {
		int accessLength = accessItem.length;
		// Create itemizedOverlay2 if it doesn't exist
		if (itemizedOverlay2 == null) {
			mapOverlays = mapView.getOverlays();
			drawable2 = this.getResources().getDrawable(
					R.drawable.accessibility);
			itemizedOverlay2 = new MyItemizedOverlay(drawable2,
					getApplicationContext());
		}
		// Add items with each click
		if (itemizedOverlay2.size() < accessLength) {
			itemizedOverlay2.addOverlay(accessItem[itemizedOverlay2.size()]);
			mapOverlays.add(itemizedOverlay2);
			// Remove all items with one click
		} else {
			for (int i = 0; i < accessLength; i++) {
				itemizedOverlay2.removeItem(accessLength - 1 - i);
			}
		}
		// Added symbols will be displayed when map is redrawn so force redraw
		// now
		mapView.postInvalidate();
	}

	// Method to insert latitude and longitude in degrees
	public static void putLatLong(double latitude, double longitude) {
		lat = latitude;
		lon = longitude;
	}

	// This sets the s key on the phone to toggle between satellite and map view
	// and the t key to toggle between traffic and no traffic view (traffic view
	// relevant only in urban areas where it is reported).

	@Override
	public boolean onKeyDown(int keyCode, KeyEvent e) {
		if (keyCode == KeyEvent.KEYCODE_S) {
			mapView.setSatellite(!mapView.isSatellite());
			return true;
		} else if (keyCode == KeyEvent.KEYCODE_T) {
			mapView.setTraffic(!mapView.isTraffic());
			mapControl.animateTo(gp); // To ensure change displays immediately
		}
		return (super.onKeyDown(keyCode, e));
	}

	// Required method since class extends MapActivity
	@Override
	protected boolean isRouteDisplayed() {
		return false; // Don't display a route
	}

}

