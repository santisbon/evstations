# EV Stations
🧪 Experimental

Source code for [@ev@botsin.space](https://botsin.space/@ev). A Mastodon bot to get electric vehicle (EV) charging stations near a location in the **United States** or **Canada**. The location needs to be specific enough to narrow it down to a relatively small area like a neighborhood. An entire city or borough won't do because it's too broad to be useful.  

## Highlights
* Mention it with just a requested location and it will reply with some charging stations near it. 
* The links provided in the results (even though they point to Apple Maps) will automatically open either Apple or Google Maps depending on your device.
* If the response doesn't fit in one post due to Mastodon's character limit it will be split into a couple of posts.
* The response includes symbols for the available connector types at each station:
  * Ⓣ Tesla aka North American Charging Standard (NACS)
  * Ⓙ J1772
  * ⒸⒸⓈ Combined Charging System (CCS) aka J1772 Combo
  * Ⓝ⑭-㊿ NEMA 14-50
  * Ⓝ⑤-⑮ NEMA 5-15
  * Ⓝ⑤-⑳ NEMA 5-20
  * ⒸⒽⒶ CHAdeMO


## Usage

Post this from your Fediverse account:
> `@ev@botsin.space` Brickell, Miami

Commas are optional, but improve performance by reducing the complexity of the search.  

**Good** query examples:  
* `60601`
* `Wrigley Field` 
* `chinatown, chicago` 
* `financial district, san francisco` 

**Bad** query examples (too big to narrow down to a ZIP/postal code):
* `nyc` 
* `Los Angeles`
* `brooklyn` 

## Limitations
* Station data including the available connector types is provided by the National Renewable Energy Laboratory at [NREL.gov](https://www.nrel.gov). It may differ from the data on Google and Apple maps. Check the station network's official website for more info.
* Tested from Mastodon and Firefish accounts. It may or may not work from other Fediverse platforms.

## Technical Documentation

### Architecture
Architecture diagrams are available in the editable svg file `architecture.drawio.svg`. You can edit it with [Draw.io](https://www.drawio.com) or simply view it below.

<details>
  <summary>Diagrams</summary>
  
  ![Diagrams](architecture.drawio.svg)

</details>

<p></p>

Reviewing the architecture diagrams and source code is a great way to learn the basics of:
* Loosely-coupled microservices.
* Message brokers with long-running producers and consumers.
* Caching.
* Container orchestration.
* Secrets management.
* Handling server-sent events from a streaming API.
* Consuming REST APIs.

You'll need a Kubernetes distribution with `dns`, `helm`, and `metrics-server` addons enabled. For a Raspberry Pi deployment you can use MicroK8s.

### Installation

You'll need to specify:
* Queue broker (RabbitMQ) configuration: Erlang cookie and password.
* Watcher configuration: password to connect to the queue broker.
* A Mastodon token with `read:statuses + read:notifications` permissions.
* Worker configuration: password to connect to the queue broker.
* A non-default user agent to comply with the geocoder's terms of service.
* A Mastodon token with `write:statuses` permissions and a post visibility setting.
* A token for the NREL.gov API.

To install/upgrade from the `solution` directory:
```sh
RELEASE=myrelease
CHART=.
NAMESPACE=mynamespace

helm dependency update

helm upgrade $RELEASE $CHART -n $NAMESPACE --create-namespace -i \
  --reuse-values \
  --set global.queue.svc=$RELEASE-rabbitmq \
  --set rabbitmq.auth.password=XXXXXXXXXX \
  --set rabbitmq.auth.erlangCookie=XXXXXXXXXX \
  --set watcher.queue.producerpassword=XXXXXXXXXX \
  --set watcher.masto.notificationtoken=XXXXXXXXXX \
  --set worker.queue.consumerpassword=XXXXXXXXXX \
  --set worker.cache.svc=$RELEASE-redis-master \
  --set worker.geocoder.useragent=mybot \
  --set worker.masto.posttoken=XXXXXXXXXX \
  --set worker.masto.visibility=direct \
  --set worker.nrel.token=XXXXXXXXXX \
```

Uninstall
```shell
helm uninstall $RELEASE -n $NAMESPACE --wait
kubectl delete namespaces $NAMESPACE
```
