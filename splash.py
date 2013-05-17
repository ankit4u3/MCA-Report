Splash XML

<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@drawable/homebg3"
    >

    <ProgressBar
        android:id="@+id/progressBar1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="right"
        android:padding="10dp" />
    
</LinearLayout>

Splash.java Source Code

package in.electromedica.in.treasurehunt;
public class Splash extends Activity {
	String build;
	String qNum, question, answer, points, latitude, longitute, hint;
	int count = 0;
	private QuestionDataSource qds;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.splashlayout);
		if (!isNetworkAvailable()) {
			Toast.makeText(this, "Need internet connection for game to start!",
					Toast.LENGTH_SHORT).show();
			finish();
		} else {
			carryOn();

		}

		// Thread timer = new Thread() {
		// @Override
		// public void run() {
		// try {
		// // if(isNetworkAvailable())
		// getDataFromJSON();
		// } catch (Exception e) {
		// e.printStackTrace();
		// } finally {
		// carryOn();
		// }
		// }
		// };
		// timer.start();

	}

	public void getDataFromJSON() {
		try {
			HttpClient client = new DefaultHttpClient();
			String getURL = MyConsts.NETWORK_FOLDER + "questions.php";

			HttpGet get = new HttpGet(getURL);
			HttpResponse responseGet = client.execute(get);
			HttpEntity resEntityGet = responseGet.getEntity();

			if (resEntityGet != null) {
				InputStream instream = resEntityGet.getContent();
				BufferedReader str = new BufferedReader(new InputStreamReader(
						instream));

				String ans = new String("");
				build = new String("");
				while ((ans = str.readLine()) != null) {
					build = build + ans;
					// Log.d(
				}

				JSONObject jobj = new JSONObject(build);
				JSONArray arr = jobj.getJSONArray("questions");
				String arrlen = Integer.toString(arr.length());
				// Log.d(
				qds = new QuestionDataSource(this);
				qds.open();
				Question q = null;
				qds.deleteAll();
				SharedPreferences prefs = PreferenceManager
						.getDefaultSharedPreferences(getBaseContext());
				SharedPreferences.Editor editor = prefs.edit();
				for (int i = 0; i < arr.length(); i++) {
					JSONObject qs = arr.getJSONObject(i);
					qNum = qs.getString("qNum");
					question = qs.getString("question");
					answer = qs.getString("answer");
					points = qs.getString("points");
					latitude = qs.getString("latitude");
					longitute = qs.getString("longitude");
					hint = qs.getString("hint"); // <= setting value
													// question
					int stat = prefs.getInt("q" + qNum, 0);
					editor.putInt("q" + qNum, stat);
					count++;
					q = qds.createQuestion(qNum, question, answer, points,
							stat, latitude, longitute, hint);
				}
				editor.putInt("count", count);
				editor.commit();
			}
		} catch (Exception e) {
			e.printStackTrace();
			Log.i("problem boy", e.getMessage());
			// Log.d(
		} finally {
			qds.close();
		}
	}

	public boolean isNetworkAvailable() {
		ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo networkInfo = cm.getActiveNetworkInfo();
		// if no network is available networkInfo will be null
		// otherwise check if we are connected
		if (networkInfo != null && networkInfo.isConnected()) {
			return true;
		}
		return false;
	}

	public void carryOn() {
		Intent i;
		// SharedPreferences useCount = getSharedPreferences("myPrefs",0);
		SharedPreferences prefs = PreferenceManager
				.getDefaultSharedPreferences(getBaseContext());
		int count = prefs.getInt("useCount", 0);
		if (count == 0) {
			i = new Intent(getApplicationContext(), UserRegistration.class);
			startActivity(i);
		} else {
			i = new Intent(getApplicationContext(), GameSelect.class);
			startActivity(i);
		}
		finish();
	}

}
