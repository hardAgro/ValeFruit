package br.edu.univasf.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import javax.annotation.PostConstruct;
import javax.faces.bean.ApplicationScoped;
import javax.faces.bean.ManagedBean;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
import org.primefaces.model.chart.Axis;
import org.primefaces.model.chart.AxisType;
import org.primefaces.model.chart.BarChartModel;
import org.primefaces.model.chart.CategoryAxis;
import org.primefaces.model.chart.ChartSeries;
import org.primefaces.model.chart.LineChartModel;

import br.edu.univasf.model.Registro;

@ManagedBean
@ApplicationScoped
public class HomeBean {

	private static final String USER_AGENT = "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion";

	private List<String> fazendas = Arrays.asList("Ouro", "Vitoria", "Conquista");
	private List<String> latitudes = Arrays.asList("-40.124575", "-40.121348", "-40.147897");
	private List<String> longitudes = Arrays.asList("-9.457124", "-9.487124", "-9.467124");
	private String contagem;

	private Random random = new Random();

	private List<Registro> registros = new ArrayList<>();

	public void novaLeitura() throws ClientProtocolException, IOException {

		analisarImagem();

		Registro novoRegistro = new Registro();
		novoRegistro.setFazenda(fazendas.get(random.nextInt(3)));
		novoRegistro.setLatitude(latitudes.get(random.nextInt(3)));
		novoRegistro.setLongitude(longitudes.get(random.nextInt(3)));
		novoRegistro.setCodigoSensor(Integer.toString(random.nextInt(10)));
		novoRegistro.setContagem(contagem);
		novoRegistro.setData(dataAtual());

		registros.add(novoRegistro);

	}

	public void analisarImagem() throws ClientProtocolException, IOException {

		String url = "http://192.168.1.139:8080/valefruitestimativa";

		HttpClient client = HttpClientBuilder.create().build();
		HttpGet request = new HttpGet(url);

		// add request header
		request.addHeader("User-Agent", USER_AGENT);
		HttpResponse response = client.execute(request);

		System.out.println("Response Code : " + response.getStatusLine().getStatusCode());

		BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));

		contagem = rd.readLine();
		System.out.println("Contage:" + contagem);
	}

	public String dataAtual() {
		LocalDateTime now = LocalDateTime.now();
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
		return now.format(formatter);
	}

	public List<Registro> getRegistros() {
		return registros;
	}

	public void setRegistros(List<Registro> registros) {
		this.registros = registros;
	}
	
}
