package com.github.ruanbekker.docker_java_springboot_hello_world.springboot.basic;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.web.bind.annotation.*;
import java.net.*;

@SpringBootApplication
@RestController

public class HelloWorld {

	public String getHostname() {
		String hostname = "";

		try {
			InetAddress inetAddress;
			inetAddress = InetAddress.getLocalHost();
			hostname = inetAddress.getHostName();
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
		return hostname;
	}

	@RequestMapping("/")
	String home() {
		return "hello from " + getHostname();
	}

    @RequestMapping("/status")
    String status() {
        return "ok";
    }

	public static void main(String[] args) throws Exception {
		SpringApplication.run(HelloWorld.class, args);
	}

}
