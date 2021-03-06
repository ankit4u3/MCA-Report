package in.electromedica.in.treasurehunt;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONObject;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.WindowManager;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

public class Leaderboard extends Activity {
	ListView lview;
	// String response;\\
	String build;
	String qNum, question, answer, points, latitude, longitute, hint;
	int count = 0;
	ArrayList<String> list;
	List<HashMap<String, String>> lmap = new ArrayList<HashMap<String, String>>();
	ProgressDialog pd;
	public WindowManager.LayoutParams lp;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.leader_layout);
		lp = getWindow().getAttributes();

		checkBrightness();
		lview = (ListView) findViewById(R.id.listViewLeaders);
		list = new ArrayList<String>();
		pd = ProgressDialog.show(Leaderboard.this, "", "Fetching leaderboard");
		pd.setCancelable(true);
		DownloadLeaders task = new DownloadLeaders();
		task.execute();

	}

	public String getLeaderData() {
		String response = "";
		try {
			HttpClient httpclient = new DefaultHttpClient();
			String connect = MyConsts.NETWORK_FOLDER + "getallusers.php";
			HttpPost httppost = new HttpPost(connect);
			HttpResponse httpResponse = httpclient.execute(httppost);
			HttpEntity resEntityGet = httpResponse.getEntity();
			if (resEntityGet != null) {
				// do something with the response
				response = EntityUtils.toString(resEntityGet);
				Log.i("GET RESPONSE", response);
				// Log.d(
				response = response.trim();

			}
		} catch (Exception e) {
			// Log.d(
			e.printStackTrace();
			// finish();
		}
		return response;
	}

	public void postLeaderData(String result) {
		getDataFromJSON();
		// StringTokenizer res = new StringTokenizer(result, ":");
		// // String[] test = {"item1","item2"};
		// while (res.hasMoreTokens()) {
		// StringTokenizer st = new StringTokenizer(res.nextToken(), ",");
		// String nick = st.nextToken(), pts = st.nextToken();
		// if (nick.equals("LIST_ENDS"))
		// break;
		// HashMap<String, String> hmap = new HashMap<String, String>();
		// hmap.put("nick", nick);
		// hmap.put("points", pts);
		// lmap.add(hmap);
		// }
		// String[] from = { "nick", "points" };
		// int[] to = { R.id.leader_tvnick, R.id.leader_tvpoints };
		// SimpleAdapter simp = new SimpleAdapter(Leaderboard.this, lmap,
		// R.layout.leaderboard_row, from, to);
		// lview.setAdapter(simp);
		// lview.setCacheColorHint(0x00000000);
	}

	public void getDataFromJSON() {
		try {
			HttpClient client = new DefaultHttpClient();
			String getURL = MyConsts.NETWORK_FOLDER + "getallusers.php";
			// String getURL = "http://flashracebits.webatu.com/questions.json";

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
				for (int i = 0; i < arr.length(); i++) {
					JSONObject qs = arr.getJSONObject(i);
					qNum = qs.getString("nick");// nick &points
					question = qs.getString("points");
					HashMap<String, String> hmap = new HashMap<String, String>();
					hmap.put("nick", qNum);
					hmap.put("points", question);
					lmap.add(hmap);

				}
				String[] from = { "nick", "points" };
				int[] to = { R.id.leader_tvnick, R.id.leader_tvpoints };
				SimpleAdapter simp = new SimpleAdapter(Leaderboard.this, lmap,
						R.layout.leaderboard_row, from, to);
				lview.setAdapter(simp);
				lview.setCacheColorHint(0x00000000);
			}
		} catch (Exception e) {

		} finally {

		}
	}

	private class DownloadLeaders extends AsyncTask<String, Void, String> {
		@Override
		protected String doInBackground(String... params) {
			String response = getLeaderData();
			return response;
		}

		@Override
		protected void onPostExecute(String result) {
			if (pd.isShowing())
				pd.dismiss();
			postLeaderData(result);
		}
	}

	@Override
	public void onBackPressed() {
		// TODO Auto-generated method stub
		finish();
		overridePendingTransition(R.anim.slide_in_top, R.anim.slide_out_bottom);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.activity_main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case R.id.menu_settings:
			Toast.makeText(this, "Can be done through Home page only.",
					Toast.LENGTH_SHORT).show();
			return true;
		case R.id.outdoorvis:
			if (MainActivity.isBright) {
				lp.screenBrightness = MainActivity.initBright;
				getWindow().setAttributes(lp);
				MainActivity.isBright = false;
			} else {
				lp.screenBrightness = 1;
				getWindow().setAttributes(lp);
				MainActivity.isBright = true;
			}

			return true;
		}
		return false;
	}

	public void checkBrightness() {
		if (!MainActivity.isBright) {
			lp.screenBrightness = MainActivity.initBright;
			getWindow().setAttributes(lp);
			MainActivity.isBright = false;
		} else {
			lp.screenBrightness = 1;
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
