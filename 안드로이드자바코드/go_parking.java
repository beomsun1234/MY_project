package com.example.test;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;

public class go_parking extends AppCompatActivity {
    ImageView handle;
    private Handler mHandler;
    private Socket socket;
    TextView tx;

    private DataOutputStream dos;
    private DataInputStream dis;
    public int ckValue = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.go_parking);

        //button = (Button)findViewById(R.id.connect);
        handle = (ImageView) findViewById(R.id.handle_1);
        tx = (TextView)findViewById(R.id.recText);

        Animation animation = AnimationUtils.loadAnimation(getApplicationContext(), R.anim.rotate);
        handle.setAnimation(animation);

    }
    @Override
    public void onStart() {
        super.onStart();
        try {
            connect();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Check if user is signed in (non-null) and update UI accordingly.
    }
    @Override
    public void onStop() {
        super.onStop();
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        // Check if user is signed in (non-null) and update UI accordingly.
    }
    void connect() throws IOException {
        mHandler = new Handler();
        Log.w("connect","연결 하는중");
        // 받아오는거
        Thread checkUpdate = new Thread() {
            public void run() {
                int ck=0;
                    // 서버 접속
                    try {
                        //socket = new Socket("192.168.55.1", 8080);
                        socket = new Socket();
                        SocketAddress addr = new InetSocketAddress("192.168.43.174", 8080/*port*/);
                        socket.connect(addr);
                        Log.w("서버 접속됨", "서버 접속됨");
                    } catch (IOException e1) {
                        Log.w("서버접속못함", "서버접속못함");
                        e1.printStackTrace();
                    }

                    Log.w("edit 넘어가야 할 값 : ", "안드로이드에서 서버로 연결요청");

                    try {
                        dos = new DataOutputStream(socket.getOutputStream());   // output에 보낼꺼 넣음
                        dis = new DataInputStream(socket.getInputStream());     // input에 받을꺼 넣어짐
                        String data = "parking";
                        dos.writeUTF(data);
                        dos.flush();
                    } catch (IOException e) {
                        e.printStackTrace();
                        Log.w("버퍼", "버퍼생성 잘못됨");
                    }
                    Log.w("버퍼", "버퍼생성 잘됨");
                        // 서버에서 계속 받아옴 - 한번은 문자, 한번은 숫자를 읽음. 순서 맞춰줘야 함.
                        try {
                            String rm = null;
                            byte[] buffer = new byte[1024];
                            int size = dis.read(buffer, 0, 1024);
                            rm = new String(buffer, 0, size);
                            Log.d("서버에서  값 ", "" + rm);
                            if(rm.equals("finsh")){
                                Log.d("종료", "종료");
                                ck=1;
                                String senddata="finsh";
                                dos.writeUTF(senddata);
                                dos.flush();
                                startFinshActivity();

                            }
                        } catch (Exception e) {
                        }
                    }

        };
        // 소켓 접속 시도, 버퍼생성
        checkUpdate.start();
        Log.d("업데이트 ","업데이트");
    }
    private  void startFinshActivity(){
        Intent intent = new Intent(this, finsh_parking.class);
        intent.addFlags(intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(intent);
    }
}

