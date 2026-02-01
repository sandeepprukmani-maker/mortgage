<template>
    <div class="col-xxl-4 col-lg-6">
        <div class="card h-100 border shadow-none">
            <div class="card-body p-24">
                <div class="d-flex align-items-center flex-wrap gap-2 justify-content-between mb-20">
                    <h6 class="mb-2 fw-bold text-lg">Total Transactions</h6>
                    <div>
                        <select class="form-select form-select-sm w-auto bg-base border text-secondary-light radius-8">
                            <option>Yearly</option>
                            <option>Monthly</option>
                            <option>Weekly</option>
                            <option>Today</option>
                        </select>
                    </div>
                </div>

                <ul class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-28">
                    <li class="d-flex align-items-center gap-2">
                        <span class="w-16-px h-16-px radius-2 bg-primary-600"></span>
                        <span class="text-secondary-light text-lg fw-normal">
                            Total Gain:
                            <span class="text-primary-light fw-bold text-lg">$50,000</span>
                        </span>
                    </li>
                </ul>

                <div id="transactionLineChart"></div>

            </div>
        </div>
    </div>
</template>

<script>
import ApexCharts from 'apexcharts';

export default {
    name: 'TotalTransactions',
    mounted() {
        var options = {
            series: [{
                name: "This month",
                data: [4, 16, 12, 28, 22, 38, 23]
            }],
            chart: {
                height: 290,
                type: 'line',
                toolbar: {
                    show: false
                },
                zoom: {
                    enabled: false
                },
                dropShadow: {
                    enabled: true,
                    top: 6,
                    left: 0,
                    blur: 4,
                    color: "#000",
                    opacity: 0.1,
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth',
                width: 3
            },
            markers: {
                size: 0,
                strokeWidth: 3,
                hover: {
                    size: 8
                }
            },
            tooltip: {
                enabled: true,
                x: {
                    show: true,
                },
                y: {
                    show: false,
                },
                z: {
                    show: false,
                }
            },
            grid: {
                row: {
                    colors: ['transparent', 'transparent'],
                    opacity: 0.5
                },
                borderColor: '#D1D5DB',
                strokeDashArray: 3,
            },
            yaxis: {
                min:0,
                max:45,
                tickAmount:5,
                labels: {
                    formatter: function (value) {
                        return "$" + value + "k";
                    },
                    style: {
                        fontSize: "14px"
                    }
                },
            },
            xaxis: {
                categories: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
                tooltip: {
                    enabled: false
                },
                labels: {
                    formatter: function (value) {
                        return value;
                    },
                    style: {
                        fontSize: "14px"
                    }
                },
                axisBorder: {
                    show: false
                },
                crosshairs: {
                    show: true,
                    width: 20,
                    stroke: {
                        width: 0
                    },
                    fill: {
                        type: 'solid',
                        color: '#B1B9C4',
                        gradient: {
                            colorFrom: '#D8E3F0',
                            colorTo: '#BED1E6',
                            stops: [0, 100],
                            opacityFrom: 0.4,
                            opacityTo: 0.5,
                        },
                    }
                }
            }
        };

        var chart = new ApexCharts(document.querySelector("#transactionLineChart"), options);
        chart.render();
    }
};
</script>