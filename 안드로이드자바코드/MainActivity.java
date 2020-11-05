package com.example.test;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import android.content.Intent;
import android.os.Handler;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.DataInputStream;
import java.io.DataOutputStream;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.io.DataOutputStream;


public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button connect;                 // ip 받아오는 버튼
    Button button2;
    ImageView handle;
    ImageView car;

    EditText ip_edit;               // ip 에디트
    TextView show_text;             // 서버에서온거 보여주는 에디트
    // 소켓통신에 필요한것
    private String html = "";
    private Handler mHandler;

    private Socket socket;
    public String pdata = "parking";
    public String ldata = "lane";

    private DataOutputStream dos;
    private DataInputStream dis;
    public int ckValue = 0;

    private String ip = "192.168.25.62";            // IP 번호
    private int port = 8080;                          // port 번호

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //button = (Button)findViewById(R.id.connect);

        findViewById(R.id.connect).setOnClickListener(onClickListener);
        findViewById(R.id.logoutButton).setOnClickListener(onClickListener);
        findViewById(R.id.laneButton).setOnClickListener(onClickListener);
        findViewById(R.id.cruiseButton).setOnClickListener(onClickListener);

        //button.setOnClickListener(this);
        //ip_edit = (EditText)findViewById(R.id.ip_edit);
        //show_text = (TextView)findViewById(R.id.show_text);
    }
    View.OnClickListener onClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            switch (v.getId()){
                case R.id.logoutButton:
                    Log.e("클릭","로그아웃버튼 클릭");
                    startLoginActivity();
                    break;
                case R.id.connect:
                    Log.e("클릭","파킹 클릭");
                    startParkingScreenActivity();
                    break;
                    //ckValue=1;
                case R.id.laneButton:
                    Log.e("클릭","라인 클릭");
                    startLaneScreenActivity();
                    break;
                    //ckValue=2;
                case R.id.cruiseButton:
                    Log.e("클릭","크루즈 클릭");
                    //ckValue=3;
                    startCruiseScreenActivity();
                    break;
                    //connect();
            }

        }
    };

    // 로그인 정보 db에 넣어주고 연결시켜야 함. //라인디텍션


    private  void startLoginActivity() {
        Intent intent = new Intent(this, Login.class);
        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }
    private  void startLaneScreenActivity() {
        Intent intent = new Intent(this, go_lane.class);
        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }
    private  void startParkingScreenActivity() {
        Intent intent = new Intent(this, go_parking.class);
        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }
    private  void startCruiseScreenActivity() {
        Intent intent = new Intent(this, go_cruise.class);
        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }

    @Override
    public void onClick(View v) {

    }
}

