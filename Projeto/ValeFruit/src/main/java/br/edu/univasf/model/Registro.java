package br.edu.univasf.model;

import java.io.Serializable;

public class Registro implements Serializable {

	private static final long serialVersionUID = 1L;

	private String codigoSensor;
	private String fazenda;
	private String latitude;
	private String longitude;
	private String data;
	private String contagem;
	
	
	public String getCodigoSensor() {
		return codigoSensor;
	}
	public void setCodigoSensor(String codigoSensor) {
		this.codigoSensor = codigoSensor;
	}
	public String getFazenda() {
		return fazenda;
	}
	public void setFazenda(String fazenda) {
		this.fazenda = fazenda;
	}
	public String getLatitude() {
		return latitude;
	}
	public void setLatitude(String latitude) {
		this.latitude = latitude;
	}
	public String getLongitude() {
		return longitude;
	}
	public void setLongitude(String longitude) {
		this.longitude = longitude;
	}
	public String getContagem() {
		return contagem;
	}
	public void setContagem(String contagem) {
		this.contagem = contagem;
	}
	public String getData() {
		return data;
	}
	public void setData(String data) {
		this.data = data;
	}
}
